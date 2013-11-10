"""
Module to train Markov model from random text.
"""

import cPickle as pickle
from model import Model, State

if __name__ == "__main__":
    with open('text.txt') as fd:
        text = fd.read()

    model = Model(3)
    model.train_model(text)

    # save model
    with open(b"save3.p", "wb") as fd:
        pickle.dump(model, fd)
    pass

