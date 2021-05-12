#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import nltk
from nltk.tokenize import sent_tokenize

def sentencizer(text):
    #from nltk.tokenize import sent_tokenize
    #sentences = sent_tokenize(text)
    sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    sentences = sent_tokenizer.tokenize(text)
    '''
    from nltk.tokenize import regexp_tokenize
    sentences = regexp_tokenize(text, r'[\s]')
    '''
    sentences_list = []
    for sentence in sentences:
        sentences_list.append(sentence)

    return sentences_list