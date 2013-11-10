# -*- coding: utf-8 -*-
"""
This modul generates text using trained model and some prefix words.
"""

import cPickle as pickle
from model import Model, State

if __name__ == "__main__":
    model = Model()
    with open("save.p", "rb") as fd:
        model._model = pickle.load(fd)

    state = u'не'
    res = [state]
    print state
    for i in xrange(100):
        state = model.get_next(state)
        if state == None:
            res.append('<None>')
            break
        res.append(state)
    print ' '.join(res)
