# coding: utf-8
"""
if text is modified with insert, while text span is not modified, this tool can align its annotations with new text again
"""
import glob
import os.path as osp
import sys
import codecs

import argparse

try:
    import annotation
except ImportError:
    import os.path
    from sys import path as sys_path
    # Guessing that we might be in the brat tools/ directory ...
    sys_path.append(os.path.join(os.path.dirname(__file__), '../../server/src'))
    import annotation


def fix_ann(ann_fn):
    orig_text= codecs.open(ann_fn.replace('.ann','.txt')).read()
    with annotation.Annotations(ann_fn) as anns:
        tbs = list(anns.get_textbounds())
        firstIndex=0
        indices = []
        for tbi, tb in enumerate(tbs):
            pos=0
            for spani, span in enumerate(tb.spans):
                new_spantext=orig_text[span[0]:span[1]]
                span_len =span[1]-span[0]
                old_spantext=tb.tail[1:-1][pos:pos+span_len]
                # santiy check
                if old_spantext!=new_spantext:
                    firstIndex = orig_text.find(old_spantext,firstIndex)
                    if firstIndex<0:
                        firstIndex = orig_text.find(old_spantext)
                    lastIndex = firstIndex+span_len
                    if firstIndex<0:
                        raise Exception('span not found:'+span)
                    tb.spans[spani]=[firstIndex,lastIndex]
                else:
                    firstIndex=span[0]
                pos+=span_len+1


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    if len(argv[1:])==0:
        print("USAGE:", argv[0], "[ANN_DIR]", file=sys.stderr)
        return 1
    
    for arg in argv[1:]:
        if osp.isfile(arg):
            annfiles= [arg]
        elif osp.isdir(arg):
            annfiles = glob.glob(osp.join(argv[1],'*.ann'))
        else:
            print("invalid argument")
            return 1

        for annfile in annfiles:
            try:
                fix_ann(annfile)
            except Exception as e:
                print(e, file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
