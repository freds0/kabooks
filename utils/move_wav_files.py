import glob
import os
import shutil
import tqdm
import argparse
import pandas as pd
import csv

def move_files(args):

    for old_file in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*" + args.files_type))):
        filename = old_file.split('/')[-1]
        new_path = '/'.join(old_file.split('/')[0:-2])
        new_file = os.path.join(new_path, args.dest_folder, filename)
        if not args.force:
            print('cp: ' + old_file + ' ' + new_file)
        else:
            os.makedirs(os.path.join(new_path, args.dest_folder), exist_ok=True)
            shutil.copy(old_file, new_file)
            #shutil.rmtree(old_folder) 
            #os.rename(new_folder, old_folder)                

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./output')  
  parser.add_argument('--files_type', default='.wav', help='Name of old wavs folder, to erase')
  parser.add_argument('--dest_folder', default='wavs', help='Name of new wavs folder')
  parser.add_argument('--force', action='store_true', default=False)
  args = parser.parse_args()

  move_files(args)


if __name__ == "__main__":
  main()
