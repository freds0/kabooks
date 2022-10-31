import argparse
from glob import glob
from tqdm import tqdm
from os.path import join, dirname
from text_tools.custom_tokenizer import infix_re
from text_tools.language_tokenizer import get_language_tokenizer
import textdistance

#from utils.nltk_sntencizer import sentencizer
#from nltk.tokenize import word_tokenize

#nlp = Portuguese()
#nlp.tokenizer.infix_finditer = infix_re.finditer

# Defining what is punctuation
punctuation = [',', '.', ';', ':', '?', '!', '—']


def find_trigram(trigram, text):

    best = 0
    i = 0
    while i < len(text):
        similarity = textdistance.ratcliff_obershelp.normalized_similarity(trigram, text[i:])
        if similarity > best:
            best = similarity
        else:
            break
        i += 1

    best = 0
    j = len(text) - 1
    while j > 0:
        similarity = textdistance.ratcliff_obershelp.normalized_similarity(trigram, text[i:j])
        if similarity > best:
            best = similarity
        else:
            break
        j -= 1

    while j<len(text) and text[j] != ' ':
        j += 1

    return j


def correct_punctuation(language_abbrev, text_clean, text_punc):
    # Defining language tokenizer
    nlp = get_language_tokenizer(language_abbrev)
    # Defining begin and end tokens
    begin_token = '# # # '
    end_token = ' *'
    text_punc = begin_token + text_punc + end_token
    # Tokeninzing punctuated text_tools.
    tokens_text_punc = nlp( begin_token + text_punc + end_token)
    # Tokenizing with nltk
    #tokens_text_punc = word_tokenize(text_punc)

    new_text = begin_token + text_clean + end_token
    for i in range(3, len(tokens_text_punc)):
        if tokens_text_punc[i].text in punctuation:
            # Get the last three tokens before the punctuation
            trigram = ' '.join([tokens_text_punc[i-j].text.lower() for j in range(3, 0, -1) ] )
            # Find the position after the trigram
            trigram_position = find_trigram(trigram, new_text)
            # Insert punctuation on new_text. Exception: before "—" must be inserted a blank space.
            punc = tokens_text_punc[i].text if tokens_text_punc[i].text != '—' else  ' ' + tokens_text_punc[i].text
            new_text = new_text[:trigram_position] + punc + new_text[trigram_position:]

    return new_text[len(begin_token) -1 : - len(end_token)] # Removing begining and ending token


def insert_punctuation_on_substring(language_abbrev, metadata_file, wavs_folder, output_filepath):
    with open(metadata_file) as f:
        content_file = f.readlines()

    input_dir = dirname(metadata_file)

    separator = '|'
    out_file = open(output_filepath, 'a')
    for line in content_file:

        filename, text_clean, text_punc, lev = line.split('|')
        #folder1, folder2, _ = filename.split('_')
        #filepath = join(input_dir, folder1, folder2, filename + '.wav')
        filepath = join(wavs_folder, filename)
        new_text = correct_punctuation(language_abbrev, text_clean.strip(), text_punc.strip())
        line = separator.join([filepath, new_text.strip(), text_punc.strip()])
        out_file.write(line + '\n')

    out_file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('-l', '--language', default='pt',
                        help='Language to download. pt: portuguese, pl: polish, it: italian, sp: spanish, fr: french, du: dutch, ge: german, en: english')
    parser.add_argument('--input_dir', default='mls_portuguese_opus')
    parser.add_argument('--csv_file', default='output_search.txt', help='Name of csv file')
    parser.add_argument('--out_file', default='output_revised.csv', help='Name of csv result ile')
    args = parser.parse_args()

    output_filepath = join(args.base_dir, args.out_file)

    out_file = open(output_filepath, 'w')
    out_file.close()
    for metadata in tqdm(glob(join(args.base_dir, args.input_dir) + '/**/**/' + args.csv_file )):
        insert_punctuation_on_substring(args.language, metadata, output_filepath)


if __name__ == "__main__":
    main()
