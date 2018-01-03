from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.util import ngrams

def frequencies(text, ngs=False, filter_stops=True):
    """
    Returns a token frequency dictionary given a large string.
    """
    tokenizer = RegexpTokenizer(r'\w+')
    tokes = tokenizer.tokenize(text.lower())
    stop = set(stopwords.words('english'))

    if ngs:
        tokes = ngrams(tokes, ngs)

    count_set = {}
    for tok in tokes:
        if filter_stops and isinstance(tok, tuple):
            cont = False
            for elem in tok:
                if elem in stop:
                    cont = True
                    break
            if cont:
                continue
        if filter_stops and tok in stop:
            continue
        if tok not in count_set:
            count_set[tok] = 0
        count_set[tok] += 1
    return count_set
    