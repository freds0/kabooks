import glob
import os
import shutil
import tqdm
import argparse
import pandas as pd
import csv

def select_files_save_delete(args):

    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*"))):
        if not os.path.exists(folder) or not os.path.isdir(folder):
            continue
        # Read input file
        metadata_file = os.path.join(folder, args.input_file)
        if not os.path.exists(metadata_file):
            return
        df = pd.read_csv(metadata_file, sep = '|', quoting=csv.QUOTE_NONE)
        # To save files
        save_file = os.path.join(folder, args.save_file)
        new_df = df[df['similarity'] >= float(args.min_value)].copy()
        new_df['transcript'] = new_df['text']
        new_df = new_df.drop(['similarity'], axis=1)
        new_df.to_csv(save_file, sep = '|', index=False, header=False, quoting=csv.QUOTE_NONE)
        # To delete files
        delete_file = os.path.join(folder, args.delete_file)
        new_df = df[df['similarity'] < float(args.min_value)].copy()
        #new_df[2] = new_df[1]
        #new_df = new_df.drop([3], axis=1)
        new_df.to_csv(delete_file, sep = '|', index=False, header=False, quoting=csv.QUOTE_NONE)
        
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')  
  parser.add_argument('--input_file', default='validation.csv')
  parser.add_argument('--save_file', default='save.csv')
  parser.add_argument('--delete_file', default='delete.csv')
  parser.add_argument('--min_value', default=0.70)

  args = parser.parse_args()
  select_files_save_delete(args)

if __name__ == "__main__":
  main()
