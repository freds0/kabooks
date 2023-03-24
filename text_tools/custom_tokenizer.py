#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Custom Spacy tokenizer
#
# (C) 2021 Frederico Oliveira, UFMT
# Released under GNU Public License (GPL)
# email fred.santos.oliveira@gmail.com
#
# Source: https://spacy.io/usage/linguistic-features#how-tokenizer-works
#import spacy
#from spacy.lang.pt import Portuguese
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

HYPHENS='-'
# Modify tokenizer infix patterns
infixes = (
    LIST_ELLIPSES
    + LIST_ICONS
    + [
        r"(?<=[0-9])[+\-\*^](?=[0-9-])",
        r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
        ),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        # ✅ Commented out regex that splits on hyphens between letters:
         r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
        #r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
    ]
)

infix_re = compile_infix_regex(infixes)
'''
nlp = Portuguese()
nlp.tokenizer.infix_finditer = infix_re.finditer

doc = nlp("Depois, com as mãos salpicadas de sangue, deixando a rês a arquejar numa poça de sangue, o piedoso homem galgou a colina, correu à cabana, gritou dentro alegre-mente:")
print([t.text_tools for t in doc]) 
'''