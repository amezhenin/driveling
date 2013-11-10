# -*- coding: utf-8 -*-
"""
This modul generates text using trained model and some prefix words.
"""

import cPickle as pickle
from model import Model, State

if __name__ == "__main__":
    with open("save2.p", "rb") as fd:
        model = pickle.load(fd)

    state = [u'не', u'мысля']
    text = list(state)
    for i in xrange(100):
        state, res = model.get_next(state)
        if res == None:
            res.append('<None>')
            break
        text.append(res)

    print ' '.join(text)
