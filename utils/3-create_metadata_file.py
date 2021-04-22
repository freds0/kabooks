import argparse
import glob
import os
import tqdm
import csv


def create_metadata_files(args):

    output_path = os.path.join(args.base_dir, args.output_file)
    if args.force:
        out_file = open(output_path, 'w')

    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*"))):
        if not os.path.isdir(folder):
            continue

        input_file = os.path.join(folder, args.input_file)
        output_internal_file = os.path.join(folder, args.output_file)

        if not os.path.exists(input_file):
            print('File ' + input_file + ' not found.')
            continue

        basename = ''

        if args.force:
            with open(input_file) as g:
                content_file = g.readlines()[1:]

            #os.rename(input_file, output_internal_file)
            for line in content_file:
                out_file.write(line)
        else:
            print('mv ' + input_file + ' ' + output_path)

    if args.force:    
        out_file.close()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./output')  
  parser.add_argument('--input_file', default='save.csv')
  parser.add_argument('--output_file', default='metadata.csv')
  parser.add_argument('--force', action='store_true', default=False)
  args = parser.parse_args()

  create_metadata_files(args)


if __name__ == "__main__":
  main()
