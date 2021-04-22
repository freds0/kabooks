import glob
import os
import tqdm
import argparse
import librosa
import soundfile as sf

def convert_audios_samplerate(input_path, output_path, new_sample_rate = 22050, execute = True):

    if execute and not(os.path.exists(output_path)):
        os.makedirs(output_path)

    for wavfile_path in tqdm.tqdm(sorted(glob.glob(input_path + "/*.wav"))):
        try:
            filename = wavfile_path.split('/')[-1]
            data, sample_rate = librosa.load(wavfile_path)
            data = data.T
            new_data = librosa.resample(data, sample_rate, new_sample_rate)

            output_file = os.path.join(output_path, filename)            

            if execute:
                sf.write(output_file, new_data, new_sample_rate)
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
  parser.add_argument('--input_folder', default='wavs')
  parser.add_argument('--output_folder', default='wavs22')
  parser.add_argument('--new_sample_rate', default=22050)
  parser.add_argument('--execute', action='store_true', default=False)
  args = parser.parse_args()

  input_path = os.path.join(args.base_dir, args.input_folder)
  output_path = os.path.join(args.base_dir, args.output_folder)
  convert_audios_samplerate(input_path, output_path, new_sample_rate=args.new_sample_rate, execute=args.execute)

if __name__ == "__main__":
  main()
