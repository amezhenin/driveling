"""
Module to train Markov model from random text.

Examples:
    python trainer.py -n 1 -o save.p -f text.txt 
    python trainer.py -n 2 -o save2.p -f text.txt
    python trainer.py -n 2 -o save3.p -u https://raw.github.com/amezhenin/driveling/master/text.txt
    python trainer.py -n 1 -o save4.p -u http://www.gnu.org/licenses/gpl-2.0.txt
"""

import cPickle as pickle
import argparse
import subprocess
from model import Model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, nargs='+',
                        help="local files to train model")
    parser.add_argument("-u", "--url", type=str, nargs='+',
                        help="url of remote files to train model")
    parser.add_argument("-n", type=int, required=True,
                        help="order of markov chain")
    parser.add_argument("-o", type=str, required=True,
                        help="file to save model")
    args = parser.parse_args()

    texts = []

    # read train text from local files
    if args.file:
        for i in args.file:
            try:
                with open(i) as fd:
                    texts.append(fd.read())
            except Exception, exc:
                print exc.strerror + ': ' + i
    # read remote files to train model
    if args.url:
        for i in args.url:
            proc = subprocess.Popen(["curl", i], stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            if err:
                print err + ": " + i
            if len(out) > 0:
                texts.append(out)

    if len(texts) == 0:
        print "Error: no train text given"
        exit()

    model = Model(args.n)
    for i in texts:
        model.train_model(i)

    # save model
    with open(args.o, "wb") as fd:
        pickle.dump(model, fd)
    pass

