# coding: UTF-8
import sys
import os
import os.path as osp
import shutil
import glob
import random

"""
 collect valid brat files and split it into train/valid folder
"""

dest_base_dir="neuroner/data/skincare_red"
 

def split_dataset(ann_dir):
    annfiles = glob.glob(osp.join(ann_dir,'part*/*.ann'))
    valid_files = []
    for ann_file in annfiles:
        if osp.getsize(ann_file)>=0:
            valid_files.append(ann_file)
    print('valid files:',len(valid_files))
    # split train/valid
    random.shuffle(valid_files)
    valid_num = len(valid_files)
    # ensure base dir is clean
    if osp.exists(dest_base_dir):
        shutil.rmtree(dest_base_dir)
    for index, ann_file in enumerate(valid_files):
        txt_file=ann_file.replace('.ann','.txt')
        if index/valid_num<0.9:
            stage='train/'
        else:
            stage='valid/'
        dest_dir = os.path.join(dest_base_dir, stage)
        shutil._ensure_directory(dest_dir)
        # move file to stage folder
        shutil.copy(ann_file, dest_dir)
        shutil.copy(txt_file, dest_dir)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    if len(argv[1:])==0:
        ann_dir='data/skincare_red'
    else:
        ann_dir=argv[1]
    if not osp.isdir(ann_dir):
        print("ANN_DIR doesn't exist", file=sys.stderr)
        return 1
    split_dataset(ann_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

 