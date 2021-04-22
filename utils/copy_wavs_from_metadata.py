import argparse
import glob
import os
import pandas as pd
import csv
import tqdm
import shutil

def copiar(args):
    total = 0     
    df = pd.read_csv(args.input_file, sep = '|', quoting=csv.QUOTE_NONE, header=None)
    if args.force:
        os.mkdir(os.path.join(args.base_dir, args.dest_folder))
    for index, row in df.iterrows():                 
        path_file = os.path.join(args.base_dir, args.wavs_folder, row[0])
        dest_path_file = path_file.replace(args.wavs_folder, args.dest_folder)
        if os.path.exists(path_file):
            total += 1
            if not(args.force):
                print(' mv {} {}'.format(path_file, dest_path_file))
            else:
                shutil.copyfile(path_file, dest_path_file)

    if args.force:    
        print('Total wav files copied: ', total)
    else:
        print('Total wav files read to be copied: ', total)  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_file', default='save.csv')
    parser.add_argument('--wavs_folder', default='wavs', help='Input wavs folder')
    parser.add_argument('--dest_folder', default='new_wavs', help='Input wavs folder')
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()
    copiar(args)

if __name__ == "__main__":
    main()
