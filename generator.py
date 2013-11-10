# -*- coding: utf-8 -*-
"""
This module generates text using trained model and some prefix words.

Examples:
    python generator.py -m save2.p -k 100 -s не мысля
    python generator.py -m save2.p -k 100 -s не мысля гордый
    python generator.py -m save2.p -k 100 -s asdf ff
    python generator.py -m save4.p -k 100 -s gnu
"""
import argparse
import cPickle as pickle
from model import Model, State

def main(model, state, k):
    if len(state) < model._n:
        print "Not enough words for initial state"
        exit()
    if len(state) > model._n:
        state = state[-model._n:]

    text = list(state)
    for i in xrange(k):
        state, res = model.get_next(state)
        if res == None:
            break
        text.append(res)

    print ' '.join(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, required=True,
                        help="file with trained model")
    parser.add_argument("-s", "--start", type=str, nargs='+', required=True,
                        help="beginning of text(initial state)")
    parser.add_argument("-k", type=int, required=True,
                        help="number of generated states")
    args = parser.parse_args()


    try:
        with open(args.model, "rb") as fd:
            model = pickle.load(fd)
    except Exception, exc:
        print "Can't load model file: " + exc.strerror
        exit()

    state = [i.decode('utf8') for i in args.start]
    main(model, state, args.k)

