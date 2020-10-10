from gensim.models.keyedvectors import KeyedVectors
from lmdb_embeddings.writer import LmdbEmbeddingsWriter
import argparse
from argparse import RawTextHelpFormatter
import functools
import codecs
import numpy as np


def parse_arguments(arguments=None):
    """
    Parse the arguments

    arguments:
        arguments the arguments, optionally given as argument
    """

    parser = argparse.ArgumentParser(description='''W2vToLmdb CLI''', formatter_class=RawTextHelpFormatter)

    parser.add_argument('--w2v_path', required=True, default=None, help='The parameters file')
    parser.add_argument('--output_path', required=False, default=None, help='by default output path is w2v dir')
    try:
        arguments = parser.parse_args(args=arguments)
    except:
        parser.print_help()
        sys.exit(0)

    # http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
    arguments = vars(arguments)

    return {k: v for k, v in arguments.items() if v is not None}


def iter_w2v_embeddings(gensim_model):
    for word in gensim_model.vocab.keys():
        yield word, gensim_model[word]

def iter_glove_embeddings(filepath):
    file_input = codecs.open(filepath, 'r', 'UTF-8')
    count = -1
    for cur_line in file_input:
        count += 1
        #if count > 1000:break
        cur_line = cur_line.strip()
        cur_line = cur_line.split(' ')
        if len(cur_line)==0:continue
        token = cur_line[0]
        vector = np.array([float(x) for x in cur_line[1:]])
        yield token, vector
    file_input.close()

def main():
    args=parse_arguments()
    w2v_path=args['w2v_path']
    assert w2v_path.endswith('.txt'), "w2v file should be txt"
    output_path= args.get('output_path', w2v_path[:-3]+'mdb')
    
    if 'glove' in w2v_path:
        iter_embeddings=functools.partial(iter_glove_embeddings,w2v_path)
    else:
        gensim_model = KeyedVectors.load_word2vec_format(w2v_path)
        iter_embeddings = functools.partial(iter_w2v_embeddings,gensim_model)
    print('Writing vectors to a LMDB database...')
    
    print(str(iter_embeddings))
    writer = LmdbEmbeddingsWriter(iter_embeddings()).write(output_path)

if __name__=="__main__":
    main()