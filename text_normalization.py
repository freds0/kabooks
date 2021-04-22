import re
import argparse
from num2words import num2words

def convert_numeral_to_word(text):
    # split the sentence into the punctuation
    sentences = re.split(r'([.,!?:;])', text)
    # split sentences into words (breaks in the blank space) and convert numeric digits to words using num2words
    sentences = [num2words(word, lang='pt_BR') if word.isdigit() else word for  phrase in sentences for word in phrase.split(' ') ]
    # concatenates everything   
    sentences = iter(sentences)
    new_sentences = next(sentences)
    for sentence in sentences:    
        if sentence in ['.', ',', '!', '?', ':', ';']:
            new_sentences += '' + sentence.strip() # concatenate two sentences
        else:
            new_sentences += ' ' + sentence.strip() # concatenate two sentences
    return new_sentences.replace('  ', ' ')

def get_number_of_words(sentence):
        # counting number of words on sentence
    length_sentence = len(sentence.split(' '))
    return length_sentence

def merge_sentences(sentences, min_words):
    '''
    found_short_sentence = True
    while(found_short_sentence):
        found_short_sentence = False
        for index, sentence in enumerate(sentences[:-1]):
            # Verify number of words on sentence
            if (len(sentence.split()) < min_words):
                found_short_sentence = True
                sentences[index:index+2] = [' '.join(sentences[index:index+2])]

    # Removing blank itens from list
    '''
    sentences = iter(sentences)
    lines, current = [], next(sentences)
    for sentence in sentences:    
        if  get_number_of_words(current) > min_words:
            lines.append(current)
            current = sentence # next
        # Concatenates sentences
        else:
            current += " " + sentence # concatenate two sentences
    lines.append(current)
    nonempty_lines = list(filter(None, lines))
    return nonempty_lines
    '''
    nonempty_sentences = list(filter(None, sentences))
    
    if len(nonempty_sentences[-1]) < min_words:
        nonempty_sentences[index-2:index-1] = [' '.join(nonempty_sentences[index-2:index-1])]
    return nonempty_sentences
    '''
def normalize_text(text):

    # Convert number to words
    text = convert_numeral_to_word(text)

    # Creating only one sentence
    text = text.replace('\n', ' ')
    text = text.strip()
    # Removing double black spaces
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def tokenize_sentences_on_punctuation(text, include_comma = False):

    # Tokenize by punctuation
    if include_comma:
        sentences = re.split(r'([.,!?:;])', text)
        # Result example: ['Capítulo I Marselha', '.', 'A Checada Em 24 de Fevereiro de 1815', ','] 
    else:
        sentences = re.split(r'([.;])', text)

    for index, sentence in enumerate(sentences[:-1]):
        sentence = sentence.strip()
        sentences[index:index+2] = [''.join(sentences[index:index+2])] # Result example: ['Capítulo I Marselha.', 'A Checada Em 24 de Fevereiro de 1815,']
    # Removing blank itens from list
    nonempty_sentences = list(filter(None, sentences))
    return nonempty_sentences

def get_size_of_biggest_sentence(sentences):
    max_length_sentence = 0
    for sentence in sentences:
        length_sentence = get_number_of_words(sentence)
        if  length_sentence > max_length_sentence:
            max_length_sentence = length_sentence
    return max_length_sentence

def text_tokenization(text, min_words, max_words):

    # Tokenize on punctuation
    sentences = tokenize_sentences_on_punctuation(text)
    # Verify lenght of sentences
    length_biggest_sentence = get_size_of_biggest_sentence(sentences)

    # Second: tokenize on special words
    if length_biggest_sentence > max_words: # very long sentence
        sentences = tokenize_sentences_on_punctuation(text, include_comma=True)
    '''
    # Concatenates small sentences
    sentences = iter(sentences)
    lines, current = [], next(sentences)
    for sentence in sentences:    
        if  get_number_of_words(current) > min_words:
            lines.append(current)
            current = sentence # next
        # Concatenates sentences
        else:
            current += " " + sentence # concatenate two sentences
    lines.append(current)
    nonempty_lines = list(filter(None, lines))
    return nonempty_lines
    '''
    lines = merge_sentences(sentences, min_words)
    return lines

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_file', default='input.txt', help='Filename to read input text')
    parser.add_argument('--output_file', default='output.txt', help='Filename to save the normalize text')
    parser.add_argument('--min_words', default=10, help='Minimal number of words on sentence')
    parser.add_argument('--max_words', default=25, help='Maximal number of words on sentence')

    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        text = file.read()

    min_words = int(args.min_words)
    max_words = int(args.max_words)

    sentences = text_tokenization(text, min_words, max_words)

    with  open(args.output_file,"w")  as f:
        for i, sentence in enumerate(sentences):
            sentence = normalize_text(sentence.strip().replace('. . .', '...'))
            f.write(sentence + '\n')


if __name__ == "__main__":
    main()
    main()
