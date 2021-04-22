import argparse
import glob
from os import makedirs
from os.path import join, exists, isdir
import csv
import tqdm

def regenerate_metadata(input_file1, basename, output_file):

    try:
        f = open(input_file1)
        content_file1 = f.readlines()
    except IOError:
      print("Error: File {} does not appear to exist.".format(input_file1))
      return False
    else:
        f.close()

    output_file = open(output_file, 'a')
    separator = '|'

    for line1 in content_file1:
        file1, text1, text2 = line1.split('|')
        filepath = join(basename, file1)
        line = separator.join([filepath, text1.rstrip(), text2.rstrip()])        
        output_file.write(line + '\n')

    output_file.close()
    return True

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='metadata_new.csv', help='Name of csv file')
    parser.add_argument('--wav_folder', default='wavs', help='Name of wavs folder')
    parser.add_argument('--internal_csv_file', default='metadata.csv', help='Name of csv file')
    args = parser.parse_args()

    separator = '|'
    output_path_file = join(args.base_dir, args.csv_file)
    output_file = open(output_path_file, 'w')
    output_file.close()

    for folder_path in tqdm.tqdm(sorted(glob.glob(args.base_dir + '/*'))):
        if not isdir(folder_path):
            continue
        foldername = join(folder_path, args.wav_folder)
        input_path_file1 = join(folder_path, args.internal_csv_file)
        regenerate_metadata(input_path_file1, foldername, output_path_file)

if __name__ == "__main__":
    main()
