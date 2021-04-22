import argparse
import glob
import os
from os import makedirs
from os.path import join, exists
from pydub import effects  
from pydub import AudioSegment
import tqdm
import shutil
#import sox
## create trasnformer
#tfm = sox.Transformer()
#tfm.norm()
#tfm.build('path/to/input_audio.wav', 'path/to/output/input_audio.wav''

def normalize_files(args):
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/"))):

        path_orig = join(folder,args.orig_dir)

        if not(exists(path_orig)):
            print('Verificar: ' + path_orig)

        shutil.rmtree(path_orig)
        path_dest = join(folder,args.dest_dir)

        if not(exists(path_dest)):
            print('Verificar: ' + path_dest)
        os.rename(path_dest, path_orig)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')
  parser.add_argument('--dest_dir', default='new_wavs', help='Name of the directory where wav files will be saved')
  parser.add_argument('--orig_dir', default='wavs', help='Name of the origin directory of wav files')
  args = parser.parse_args()
  normalize_files(args)

if __name__ == "__main__":
  main()
