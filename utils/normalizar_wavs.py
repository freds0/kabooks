import argparse
import glob
import os
from os import makedirs
from os.path import join, exists
from pydub import effects  
from pydub import AudioSegment
import tqdm
#import sox
## create trasnformer
#tfm = sox.Transformer()
#tfm.norm()
#tfm.build('path/to/input_audio.wav', 'path/to/output/input_audio.wav''

def normalize_files(args):
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/"))):
        path_orig = join(folder,args.orig_dir)
        path_dest = join(folder,args.dest_dir)

        if not(exists(path_dest)):
            makedirs(path_dest)

        for path_file in glob.glob(path_orig + "/*" + args.files_type):
    #        _sound = AudioSegment.from_file(path_file, "wav")  
    #        sound = effects.normalize(_sound)  
            filename = path_file.split('/')[-1]
    #        sound.export(join(path_dest, filename), format="wav")
            dest_file = join(path_dest, filename)
            os.system("sox -S  %s %s gain -n -3"% (path_file, dest_file))
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')
  parser.add_argument('--dest_dir', default='new_wavs', help='Name of the directory where wav files will be saved')
  parser.add_argument('--orig_dir', default='wavs', help='Name of the origin directory of wav files')
  parser.add_argument('--files_type', default='.wav', help='Name of old wavs folder, to erase')
  args = parser.parse_args()
  normalize_files(args)

if __name__ == "__main__":
  main()
