import argparse
from os.path import isfile, join, dirname
import pandas as pd
import os
import csv
import tqdm
import glob

def delete_wavs(args):

    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*"))):
        
        if not os.path.isdir(folder):
            continue
        metadata = os.path.join(folder, args.csv_file)

        # check if size of file is 0
        if os.stat(metadata).st_size == 0:
            continue
        df = pd.read_csv(metadata, sep = '|', header=None, quoting=csv.QUOTE_NONE)

        total = 0
        total_deleted = 0

        for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
            path_file = os.path.join(folder,row[0])
            #print(row)
            if os.path.exists(path_file):
                total_deleted += 1
                if not(args.erase):
                    print(path_file)
                else:
                    os.remove(path_file)
            else:
                print('error')

        if not(args.erase):
            print('Total wavs to be deleted: ', total_deleted)
        else:
            print('Total wavs deleted: ', total_deleted)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='delete.csv', help='Name of csv file')
    parser.add_argument('--erase', action='store_true', default=False)
    args = parser.parse_args()
    delete_wavs(args)

if __name__ == "__main__":
    main()
