datagger
========

A Simple Dialog Act Tagger
=======

This project intends to tag the dialog act given a discourse.

### Introduction
The corpus we used is from loria.fr. The corpus is used for a French Learnig dialog system.
You can check corpus/sample to have a feeling about how the data looks like.

### Software Depends
To use datagger, you need to install:
* NLTK: NLTK is a leading platform for building Python programs to work with human language data. http://nltk.org/
* CRF++: CRF++ is a simple, customizable, and open source implementation of Conditional Random Fields (CRFs) for segmenting/labeling sequential data. http://crfpp.googlecode.com/svn/trunk/doc/index.html
* scikit-learn: sickit-learn is python package for machine learning. http://scikit-learn.org/stable/
* KEA: KEA is a French tokenzier. https://github.com/boudinfl/kea

### Howto
You can simply run 
```bash
python2 Corpusbuilder --help
usage: CorpusBuilder.py [-h] [--cv] [--path PATH] corpuspath {crf,sample}

positional arguments:
  corpuspath    The path to the corpus
  {crf,sample}  select what kind of corpus to generate. sample: to generate
                unlabled data. crf: to build training and test data for crf

optional arguments:
  -h, --help    show this help message and exit
  --cv          build cross_validation corpus
  --path PATH   place to put the generated corpus data
```
to check the usage of the script. 

After you genrate the CRF++ data format.
Simply use
```bash
crf_learn template train_data model`
```
you will get a model file.
Use this model to tag test data, run
```bash
crf_test model test_data`
```
### Evaluation`
To evaluate our result, you can use the scipt from conll phrase recognition task. http://www.cnts.ua.ac.be/conll2000/chunking/output.html
To evaluate our result, run:
```bash
perl conlleval.pl -r -d '\t'` < result_you_got
```
`
