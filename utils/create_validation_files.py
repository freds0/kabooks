import argparse
import glob
import os
import tqdm
import csv
import sys

root = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(root)

from validation import create_validation_file

def create_all_validation_files(args):

    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*"))):
        if not os.path.isdir(folder):
            continue

        input_file1 = os.path.join(folder, args.input_file1)
        if not os.path.exists(input_file1):
            print('File ' + input_file1 + ' not found.')
            continue
        input_file2 = os.path.join(folder, args.input_file2)
        if not os.path.exists(input_file2):
            print('File ' + input_file2 + ' not found.')
            continue
        basename = ''
        output_file = os.path.join(folder, args.output_file)
        if args.execute:
            create_validation_file(input_file1, input_file2, basename, output_file)
        else:
            print(input_file1)
            print(input_file2)
            print(output_file)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')  
  parser.add_argument('--input_file1', default='metadata.csv')
  parser.add_argument('--input_file2', default='transcription.csv')
  parser.add_argument('--output_file', default='validation.csv')
  parser.add_argument('--execute', action='store_true', default=False)
  args = parser.parse_args()

  create_all_validation_files(args)


if __name__ == "__main__":
  main()
