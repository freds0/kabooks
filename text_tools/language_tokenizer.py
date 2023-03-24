import spacy
from text_tools.custom_tokenizer import infix_re
from spacy.lang.pt import Portuguese
from spacy.lang.pl import Polish
from spacy.lang.es import Spanish
from spacy.lang.it import Italian
from spacy.lang.en import English


def get_language_tokenizer(language_abbrev = 'pt'):
    if language_abbrev == 'pt':
        nlp = Portuguese()
    elif language_abbrev == 'pl':
        # nlp = spacy.load("pl_core_news_sm")
        nlp = Polish()
    elif language_abbrev == 'it':
        # nlp = spacy.load("it_core_news_sm")
        nlp = Italian()
    elif language_abbrev == 'sp':
        # nlp = spacy.load("es_core_news_sm") # or spacy.load("es_core_news_md")
        nlp = Spanish()
    elif language_abbrev == 'fr':
        nlp = spacy.load("fr_core_news_sm")
    elif language_abbrev == 'du':
        nlp = spacy.load("nl_core_news_sm")
    elif language_abbrev == 'ge':
        nlp = spacy.load("de_core_news_sm")
    elif language_abbrev == 'en':
        # nlp = spacy.load("en_core_web_sm")
        nlp = English()
    else:
        print('Language {} invalid!'.format(language_abbrev))
        return False

    nlp.tokenizer.infix_finditer = infix_re.finditer
    nlp.max_length = 9990000  # or any large value, as long as you don't run out of RAM

    return nlp