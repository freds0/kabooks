#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import spacy
from spacy.language import Language

@Language.component("custom_sentencizer")
def custom_sentencizer(doc):
    '''
    https://spacy.io/usage/processing-pipelines#custom-components
    '''
    punctuation = ',.;:?!'
    for i, token in enumerate(doc[:-2]):
        # Define sentence start if pipe + titlecase token
        if token.text in punctuation:
            doc[i + 1].is_sent_start = True
        else:
            # Explicitly set sentence start to False otherwise, to tell
            # the parser to leave those tokens alone
            doc[i + 1].is_sent_start = False
    return doc

def sentencizer(text):
    '''
    https://ashutoshtripathi.com/2020/05/04/how-to-perform-sentence-segmentation-or-sentence-tokenization-using-spacy-nlp-series-part-5/
    '''

    nlp = spacy.load("pt_core_news_md")
    nlp.add_pipe("custom_sentencizer", before="parser")

    doc = nlp(text)
    #for sentence in doc.sents:
    #    print('{} #\n'.format(sentence))
    sentences_list = []
    for sentence in doc.sents:
        #print('{} #\n'.format(sentence))
        sentences_list.append(sentence)
    return sentences_list