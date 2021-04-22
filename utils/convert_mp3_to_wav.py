import glob
import os
import tqdm
import argparse
import csv
from pydub import AudioSegment

def convert_audios_samplerate(input_path, output_path, execute = True):

    if execute and not(os.path.exists(output_path)):
        os.makedirs(output_path)

    for wavfile_path in tqdm.tqdm(sorted(glob.glob(input_path + "/*.mp3"))):
        try:
            filename = wavfile_path.split('/')[-1]
            #print(filename)
            sound = AudioSegment.from_mp3(wavfile_path)
            #data, sample_rate = librosa.load(wavfile_path)
            #data = data.T
            #data_16k = librosa.resample(data, sample_rate, new_sample_rate)
            #output_file = join(output_path, filename)
            output_file = os.path.join(output_path, filename.replace('mp3', 'wav'))            
            #sf.write(output_file, data_16k, new_sample_rate)
            if execute:
                sound.export(output_file, format="wav")
            else:
                print('In: ' + wavfile_path)
                print('Out: ' + output_file)
        except:
            print('erro converting ' + wavfile_path)
            return False

    return True

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')  
  parser.add_argument('--input_folder', default='mp3', help='Name of old wavs folder, to erase')
  parser.add_argument('--output_folder', default='wavs', help='Name of new wavs folder')
  parser.add_argument('--execute', action='store_true', default=False)
  args = parser.parse_args()

  input_path = os.path.join(args.base_dir, args.input_folder)
  output_path = os.path.join(args.base_dir, args.output_folder)

  convert_audios_samplerate(input_path, output_path, args.execute)

if __name__ == "__main__":
  main()
