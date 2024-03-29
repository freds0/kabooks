#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dado a transcricao de um arquivo, busca a frase mais proxima dentro de um texto completo.
#
# (C) 2021 Frederico Oliveira, UFMT
# Released under GNU Public License (GPL)
# email fred.santos.oliveira@gmail.com
#
import argparse
import re
import tqdm
import textdistance
import collections
#import multiprocessing
#from multiprocessing import Process, Queue
import string
from cleantext import clean
from text_tools.text_normalization import customized_text_cleaning
from text_tools.language_tokenizer import get_language_tokenizer
from os.path import join

PUNCTUATION = string.punctuation + '—'

#nlp = Portuguese()
#nlp.tokenizer.infix_finditer = infix_re.finditer


def remove_punctuations(text):
    # Remove punctuations
    text = text.translate(str.maketrans("", "", PUNCTUATION)).strip()
    return text


def preprocess_string(text):
    '''
    Auxiliar fucntion. Convert text_tools to lower case, remove the punctuation and spaces. After preprocessing you will have the text_tools as a single string, with no spaces between words.

        Parameters:
        text_tools (str): normal text_tools.

        Returns:
        String: returns text_tools preprocessed.
    '''
    # Convert to lower
    text = text.lower()
    text = remove_punctuations(text)
    # Remove blank spaces
    text = text.replace(" ", "")
    # Remove newlines
    text = re.sub('\n', '', text)
    return text.strip()


def text_cleaning(text):
    text = clean(
                text,
                fix_unicode=True,  # fix various unicode errors
                to_ascii=False,  # transliterate to closest ASCII representation
                lower=False,  # lowercase text_tools
                no_line_breaks=True,  # fully strip line breaks as opposed to only normalizing them
                no_urls=False,  # replace all URLs with a special token
                no_emails=False,  # replace all email addresses with a special token
                no_phone_numbers=False,  # replace all phone numbers with a special token
                no_numbers=False,  # replace all numbers with a special token
                no_digits=False,  # replace all digits with a special token
                no_currency_symbols=False,  # replace all currency symbols with a special token
                no_punct=False,  # remove punctuations
                replace_with_punct="",  # instead of removing punctuations you may replace them
                replace_with_url="<URL>",
                replace_with_email="<EMAIL>",
                replace_with_phone_number="<PHONE>",
                replace_with_number="<NUMBER>",
                replace_with_digit="0",
                replace_with_currency_symbol="<CUR>",
                lang="en"  # set to 'de' for German special handling
            )
    text = customized_text_cleaning(text)
    return text


def compare_char_by_char(substring, complete_string, similarity_metric='hamming'):
    '''
    Auxiliar fucntion. Checks word by word if a substring is contained in a complete text_tools, ignoring the punctuation and capital letters.

        Parameters:
        substring (str): phrase to be searched for in the complete text_tools.
        complete_text (str): complete text_tools that has a phrase similar to the substring.

        Returns:
        String: returns the phrase if it found a similar phrase, otherwise it returns False
    '''

    j = int(0.9 * len(substring))

    #count = lambda l1, l2: sum([1 for x in l1 if x in l2])
    #num_punctutations = count(complete_string[:j].text, set(PUNCTUATION))
    #j += num_punctutations

    min_similarity = 0.15
    if similarity_metric == 'ratcliff':
        min_similarity = 0.9

    best_similarity = 0.0
    while j < len(complete_string):

        # Ignores punctuation at complete_string
        if complete_string[j].text in PUNCTUATION:
            j += 1
            continue

        # Transforms the string into a single string without spaces
        sentence1 = preprocess_string(substring.text)
        sentence2 = preprocess_string(complete_string[:j].text)

        if similarity_metric == 'ratcliff':
            similarity = textdistance.ratcliff_obershelp.normalized_similarity(sentence1, sentence2)
        else:
            similarity = textdistance.hamming.normalized_similarity(sentence1, sentence2)

        if similarity < min_similarity:
            return False

        if similarity >= best_similarity:
            best_similarity = similarity
            j += 1
        else:
            j -= 1
            break

    # Necessary when it has a punctuation at begining
    i = 0
    while complete_string[i].text in PUNCTUATION:
        i += 1

    return complete_string[i:j]


def search_substring_by_char(language_abbrev, substring, complete_text, similarity_metric='hamming', start_position=0):

    print('Searching by char...')
    nlp = get_language_tokenizer(language_abbrev)
    substring = nlp(substring)
    complete_text = nlp(complete_text)

    length_complete_text = len(complete_text)
    length_substring = len(substring)

    best_similarity = 0.0
    best_substring_found = False
    #TODO: Corrigir start_position
    start = start_position
    extra_words = 15  # it is necessary to add extra words, because the punctuation is also counted.
    new_start = start
    # Iterates over the complete text_tools from position zero, increasing the initial position.
    for start in range(start_position, length_complete_text - length_substring):

        # Defines the starting position in which to search for substring
        complete_text_tmp = complete_text[start: start + length_substring + extra_words]

        # Performs the comparison of the two sentences, inserting each word in the complete_text_tmp
        substring_found = compare_char_by_char(substring, complete_text_tmp, similarity_metric)

        if substring_found:
            # In this comparison it is better to use levenshtein distance because it has better accuracy.
            similarity = textdistance.levenshtein.normalized_similarity(preprocess_string(substring.text),
                                                                        preprocess_string(substring_found.text))
            # Updates the best string found.
            if similarity >= best_similarity:
                best_similarity = similarity
                best_substring_found = substring_found.text

            # Break if it find a phrase with great similarity of words.
            if best_similarity >= 0.98:
                new_start = start
                break

    return best_substring_found, best_similarity, new_start


def execute_threads_search_substring_by_char(language_abbrev, substring, complete_text, start_position = 0, similarity_metric='hamming'):

    string_result, similarity, start_position = search_substring_by_char(language_abbrev, substring, complete_text, similarity_metric, start_position)
    return string_result, similarity, start_position


def compare_word_by_word(substring, complete_string, similarity_metric='hamming'):
    '''
    Auxiliar fucntion. Checks word by word if a substring is contained in a complete text_tools, ignoring the punctuation and capital letters.

        Parameters:
        substring (str): phrase to be searched for in the complete text_tools.
        complete_text (str): complete text_tools that has a phrase similar to the substring.

        Returns:
        String: returns the phrase if it found a similar phrase, otherwise it returns False
    '''
    min_similarity = 0.5  # minimal similarity between the words tested with hamming

    i = 0  # substring index iterator
    j = 0  # complete_string index iterator
    start = 0

    steps = 0
    max_steps = 3

    # i iterate over the variable "substring" and j iterate over the variable "complete_string"
    while i < len(substring) and j < (len(complete_string)):

        # Necessary when it has a punctuation at begining
        if i == 0 and complete_string[j].text in PUNCTUATION:
            j += 1
            start += 1
            continue

        # Ignores punctuation at substring
        if substring[i].text in PUNCTUATION:
            i += 1
            continue

        # Ignores punctuation at complete_string
        if complete_string[j].text in PUNCTUATION:
            j += 1
            continue

        # Preprocesses the two words to calculate the similarity
        word1 = substring.text.lower()
        word2 = complete_string[:j].text.lower()

        if similarity_metric == 'levenshtein':
            similarity = textdistance.levenshtein.normalized_similarity(word1, word2)
        else:
            similarity = textdistance.hamming.normalized_similarity(word1, word2)

        '''
        if similarity < min_similarity and steps <= max_steps:
            steps += 1
            j += 1
        # word1 does not match the word2, but it still returns the found string not including word2 .
        elif similarity < min_similarity and steps >= max_steps:
            return complete_string[start: j]
        '''
        if similarity < min_similarity:
            return complete_string[start: j]

        i += 1
        j += 1

    return complete_string[start: j]


def search_substring_by_word(language_abbrev, substring, complete_text, similarity_metric='hamming', start_position=0):

    print('Searching by word...')
    nlp = get_language_tokenizer(language_abbrev)
    substring = nlp(substring)
    complete_text = nlp(complete_text)

    length_complete_text = len(complete_text)
    length_substring = len(substring)

    best_similarity = 0.0
    best_substring_found = False
    #TODO: Corrigir start_position
    new_start = start_position

    # Iterates over the complete text_tools from position zero, increasing the initial position.
    for start in range(start_position, length_complete_text - length_substring):

        # Defines the starting position in which to search for substring
        complete_text_tmp = complete_text[start:]

        # Performs the comparison of each word in the sequence
        substring_found = compare_word_by_word(substring, complete_text_tmp, similarity_metric)

        # In this comparison it is better to use levenshtein distance because it has better accuracy.
        similarity = textdistance.levenshtein.normalized_similarity(
            remove_punctuations(substring.text.lower()),
            remove_punctuations(substring_found.text.lower())
        )
        # Updates the best string found.
        if similarity >= best_similarity:
            best_similarity = similarity
            best_substring_found = substring_found.text

        # Break if it find a phrase with minimal similarity of words. Comment if you desire search for all text_tools
        if best_similarity >= 0.90:
            new_start = start
            break

    return best_substring_found, best_similarity, new_start


def execute_threads_search_substring_by_word(language_abbrev, substring, complete_text, start_position = 0, similarity_metric='hamming'):

    string_result, similarity, start_position = search_substring_by_word(language_abbrev, substring, complete_text, similarity_metric, start_position)
    return string_result, similarity, start_position


def get_transcripts(transcripts_text):
    transcripts_dict = {}
    for line in transcripts_text:
        filename, text = line.split('|')
        transcripts_dict[filename] = text.strip()
    # Sorting dict by key (filename)
    ordered_transcripts_dict = collections.OrderedDict(sorted(transcripts_dict.items()))
    return ordered_transcripts_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-o', '--output_file', default='./output/result.csv')
    parser.add_argument('-l', '--language', default='pt',
                        help='Options: pt (portuguese), pl (polish), it (italian), sp (spanish), fr (french), du (dutch), ge (german), en (english)')
    parser.add_argument('-m', '--metric', default='hamming', help='Options: hamming (low accuracy, low computational cost), levenshtein (high accuracy, high computational cost) or ratcliff (average accuracy, average computational cost)')
    parser.add_argument('-i', '--input_transcripts_file', default='./output/transcription.csv')
    parser.add_argument('-c', '--complete_text_file', default='./input/complete_text.txt')
    parser.add_argument('-t', '--search_type', default='char', help='Options: word or char')
    parser.add_argument('-s', '--sequenced_text', action='store_true', default=False)

    args = parser.parse_args()
    # Load input files
    transcript_file = join(args.base_dir, args.input_transcripts_file)
    complete_text_file = join(args.base_dir, args.complete_text_file)

    output_f = open(args.output_file, "w")

    with open(transcript_file) as f:
        transcripts_text = f.readlines()

    with open(complete_text_file) as f:
        book_text = f.read()

    # Cleaning complete text_tools
    book_text = text_cleaning(book_text)

    start_position = 0
    separator = '|'
    total_similarity = 0

    # Create ordered dict from trascripts list
    transcripts_dict = get_transcripts(transcripts_text)

    # Iterates over each transcription
    for filename, text in tqdm.tqdm(transcripts_dict.items()):
        print('Processing {}'.format(filename))

        if args.search_type == 'char':
            text_result, similarity, start_position = execute_threads_search_substring_by_char(args.language, text, book_text, start_position=0, similarity_metric='hamming')
        else:
            text_result, similarity, start_position = execute_threads_search_substring_by_word(args.language, text, book_text, start_position=0, similarity_metric='hamming')

        if not text_result:
            text_result = ''
        total_similarity += similarity
        # Debug
        print(text.strip())
        print(text_result.strip())
        print(similarity)
        line = separator.join([filename.strip(), text.strip(), text_result.strip(), str(similarity) + '\n'])
        output_f.write(line)

    print('Similaridade Media: {}'.format(total_similarity / len(transcripts_text)))
    output_f.close()

if __name__ == "__main__":
    main()
