"""
Module to train Markov model from random text.
"""
import string
import cPickle as pickle
from model import Model, State

def remove_punct(text):
    return text.translate(string.maketrans("", ""), string.punctuation)

if __name__ == "__main__":
    with open('text.txt') as fd:
        text = fd.read()

    # remove punctuation
    text = remove_punct(text)
    text = text.decode('utf-8').lower()
    words = text.split()

    # building model
    prev = words.pop(0)
    model = Model()
    for i in words:
        model.train(prev, i)
        prev = i

    # save model
    with open(b"save.p", "wb") as fd:
        pickle.dump(model._model, fd)
    pass

