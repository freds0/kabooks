import argparse
import glob
from os import makedirs
from os.path import join, exists
import requests
import json
import tqdm
import sys, os

def get_transcript(wavefile_path):
        files_data = {'file': open(wavefile_path, 'rb')} 
        try:
            res = requests.post(url='https://your_custom_asr_api_link_here',
                                files=files_data)
            res.encoding='utf-8'
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected!")
            exit()
        except:
            return False
        return res.text

def transcribe_audios(input_path, output_file):
    with open(output_file, 'w') as out:
        for wavfile_path in tqdm.tqdm(sorted(glob.glob(input_path + "/*.wav"))):
            filename = wavfile_path.split('/')[-1]
            text = ''
            for attempts in range(4):
                if attempts != 0:
                    print('Attempt - {}...'.format(attempts))

                transcript = get_transcript(wavfile_path)

                try:
                    transcript_json = json.loads(str(transcript))
                    text = transcript_json['texto']
                    break

                except KeyboardInterrupt:
                    print("KeyboardInterrupt detected!")
                    exit()
                except:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    exc_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Transcribing error: ")
                    print(exc_type, exc_file, exc_tb.tb_lineno)
                
            out.write("{}|{}\n".format(str(filename),str(text)))
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--transcription_file', default='transcription.txt', help='Filename to save the transcripts')
    parser.add_argument('--input_dir', default='input', help='Input audio folder')
    parser.add_argument('--output_dir', default='output', help='Output folder of transcript file')
    args = parser.parse_args()

    input_path = join(args.base_dir, args.input_dir)
    output_file = join(args.base_dir, args.output_dir, args.transcription_file)
    transcribe_audios(input_path, output_file)

if __name__ == "__main__":
    main()
