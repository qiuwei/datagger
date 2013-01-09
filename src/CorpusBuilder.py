#!/usr/bin/python2
#-*- code=utf-8 -*-
import re
import io
import os
import kea
import argparse
import random
from nltk import tokenize
from nltk import data
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

class CorpusBuilder:
    '''
    Build corpus from the plain discourse text
    '''
    # use to store the parsed corpus
    # a corpus is a list of dialog
    # dialog will can be considered as the training unit
    # each dialog contains a list of utterance
    # each utterance is a tuple (agent, content, tag)
    # where
    # agent denotes the speaker, it will be either mina the cat or learner
    # content is the real content of utterance
    # tag is the dialog act

    _corpus = []
    vectorizer = None
    def __init__(self):
        pass

    def _build(self, filename):
        '''
        it would read in a dialog from a single file
        the input is the name(path) of the file
        out put is a list of utterance
        '''
        dialog = []
        with io.open(filename, 'r', encoding='utf-8') as dialogfile:
            next(dialogfile)
            r = re.compile(r"^>(.*?):(.*?)\s\|\|\|\|\s(.*?)$")
            for line in dialogfile:
                m = r.match(line)
                if m:
                    dialog.append((m.group(1), m.group(2), m.group(3)))
        self._corpus.append(dialog)

    def build(self, dirname):
        '''
        it walk over all of the dialog file in certain directory
        and build the corpus
        '''
        for root, dirs, files in os.walk(dirname):
            for f in files:
                #print f
                self._build(os.path.join(root, f))
        self._build_vsm()

    def _build_vsm(self):
        '''
        build vsm model for feature extraction
        extract features of speech content aka dialog[1]
        in this method, 1 gram and 2 gram features will be extracted.
        other features will be extracted:
            1.number of sentences
            2.whether the sentence is a question. if it contains several questions, then we will only consider the last sentence

        '''


        content_corpus = [u[1] for dialog in self._corpus for u in dialog]
        #import ipdb;ipdb.set_trace()
        sw = stopwords.words('french')
        uni_sw = [w.decode('utf-8') for w in sw]
        ftokenzier = kea.tokenizer()
        vectorizer = CountVectorizer(min_df=1, ngram_range=(1,1), stop_words=uni_sw, tokenizer=(lambda x : ftokenzier.tokenize(x)))
        term_document = vectorizer.fit_transform(content_corpus)
        #print term_document.toarray()
        #print u'bon' in vectorizer.get_feature_names()
        #self.analyze = vectorizer.build_analyzer()
        self.vectorizer = vectorizer


    def build_crf_corpus(self, percetage = 0.9):
        # Todo: shuffle or not
        print "The number of features is {}".format(str(len(self.vectorizer.get_feature_names())))
        trainlen = int(len(self._corpus) * 0.9)
        corpus_train = self._corpus[:trainlen]
        corpus_test = self._corpus[trainlen:]
        self._build_crf_corpus_help(corpus_train, 'train.data')
        self._build_crf_corpus_help(corpus_test, 'test.data')

    def get_unlabeld_corpus(self, percentage = 0.05):
        random.shuffle(self._corpus)
        for dialog in self._corpus[:int(len(self._corpus) * 0.05)]:
            for u in dialog:
                print u">{0}:{1} ||||".format(u[0], u[1]).encode('utf8')
            print


    def _build_crf_corpus_help(self, corpus, outfilename):
        emp = "\t"
        with open(outfilename, 'w') as outfile:
            for dialog in corpus:
                for utterance in dialog:
                    line = utterance[0]
                    line += emp
                    line += 'multi' if len(self._split_sentence(utterance[1])) > 1 else 'single'
                    line += emp
                    line += 'q' if self._is_question(utterance[1]) else 's'
                    line += emp
                    l = self.vectorizer.transform([utterance[1]]).toarray()[0]
                    line += emp.join(str(i) for i in l)
                    line += emp
                    line += utterance[2] + os.linesep
                    outfile.write(line)
                outfile.write(os.linesep)

    #def _tag_nomarlize(self, s):
    #    '''
    #    this function normalize the tag
    #    because the tag contains brackets and comma, though CRF++ can treat it correctly,
    #    the evaluation tool cannot deal with it.
    #    '''
    #    return re.sub(r'[,()]', '_', s)



    def _split_sentence(self, s):
        '''
        sentence splitter
        '''
        #use French sentence tokenizer from nltk
        pst = data.load("tokenizers/punkt/french.pickle")
        return pst.tokenize(s)

    def _is_question(self, s):
        if re.search(r"\?\s*?$", s):
            return True
        else:
            return False



def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("corpuspath", help="The path to the corpus")
    argParser.add_argument("build", choices=['crf','sample'], help='''select what kind of corpus to generate.
                           \n sample: to generate unlabled data.
                           \n crf: to build training and test data for crf''')
    args = argParser.parse_args()
    cb = CorpusBuilder()
    cb.build(args.corpuspath)
    if args.build == "crf":
        cb.build_crf_corpus()
    elif args.build == "sample":
        cb.get_unlabeld_corpus()

    # test
    #for dialog in cb._corpus:
    #    for utterance in dialog:
    #        print utterance
    #    print "===="

if __name__ == '__main__':
    main()
