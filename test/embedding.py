from lmdb_embeddings.reader import LruCachedLmdbEmbeddingsReader
from lmdb_embeddings.exceptions import MissingWordError


def test_glove_embeddings():
    token_to_vector = LruCachedLmdbEmbeddingsReader(r'd:/models/word2vec/glove.6B/glove.6B.50d/')
    word="sigarms"
    print(word,token_to_vector.get_word_vector(word).shape)

def test_tencent_embeddings():
    token_to_vector = LruCachedLmdbEmbeddingsReader(r'D:/models/word2vec/Tencent_AILab_ChineseEmbedding/lmdb')
    word="磨砂"
    print(word,token_to_vector.get_word_vector(word).shape)
    