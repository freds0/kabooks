import argparse
import glob
from os import makedirs
from os.path import join, exists
import librosa
import soundfile as sf
import tqdm

import warnings
warnings.filterwarnings('ignore')

new_sample_rate = 16000
audio_files_type = 'wav'

def convert_audios_samplerate(args):
    input_path = join(args.base_dir, args.input_dir)
    output_path = join(args.base_dir,args.output_dir)

    if not(exists(output_path)):
        makedirs(output_path)

    for wavfile_path in tqdm.tqdm(sorted(glob.glob(input_path + "/*." + audio_files_type))):

        filename = wavfile_path.split('/')[-1].replace(audio_files_type, 'wav')
        output_file = join(output_path, filename)
        if exists(output_file):
            continue
        data, sample_rate = librosa.load(wavfile_path)
        #data, sample_rate = sf.read(wavfile_path, dtype='float32')
        data = data.T
        data_16k = librosa.resample(data, sample_rate, new_sample_rate)

        #librosa.output.write_wav(output_file, data_16k, output_sample_rate)
        #sf.write(output_file, data, output_sample_rate, subtype='PCM_24')
        sf.write(output_file, data_16k, new_sample_rate)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')
  parser.add_argument('--input_dir', default='wavs', help='Directory of wav files')
  parser.add_argument('--output_dir', default='wavs_16k', help='Directory to save wav files with sample rate (16k)')
  args = parser.parse_args()
  convert_audios_samplerate(args)

if __name__ == "__main__":
  main()
