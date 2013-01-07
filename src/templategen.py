#!/usr/bin/python2
# -*- code=utf-8 -*-

import argparse
def templategen(featurenum):
    '''
    generate uniry template for crf++
    '''

    for i in range(3, 3+featurenum):
        id = 1000-i
        print "U{0}:%x[0,{1}]".format(str(id),str(i))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num", type=int, help="number of feature aka the dimension of the bag of words model")
    args = parser.parse_args()
    templategen(args.num)

if __name__ == '__main__':
    main()

