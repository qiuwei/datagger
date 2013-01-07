#!/usr/bin/python2
# -*-code=utf-8-*-

from __future__ import division
import argparse
import re

def eval(filename):
    '''
    evaluate the result
    calculate precision
    '''
    count = 0
    rightnum = 0
    with open(filename) as f:
        for line in f:
            if not re.match(r"^\s*$", line):
                count += 1
                l = line.split('\t')
                (gold, res) = (l[-2], l[-1][:-1])
                if gold == res:
                    rightnum += 1
        return rightnum/count

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", help="the name of the result file")
    args = argparser.parse_args()
    print "The precision is {}".format(str(eval(args.filename)))

if __name__ == "__main__":
    main()

