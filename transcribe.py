#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import argparse
import sys
from os import makedirs
from os.path import join, exists, basename, split
from glob import glob
from tqdm import tqdm
import librosa
import requests
import soundfile as sf
import json


def convert_audios_samplerate(input_path, output_path, new_sample_rate):
    """
    Converts all audio files within a folder to a new sample rate.
        parameters:
            input_path: input folder path with wav files.
            output_path: output folder path to save converted wav files.

        Returns:
            Boolean: True of False.
    """

    if not(exists(output_path)):
        makedirs(output_path)

    for wavfile_path in tqdm(sorted(glob(input_path + "/*.wav"))):
        try:
            filename = basename(wavfile_path)
            data, sample_rate = librosa.load(wavfile_path)
            data = data.T
            new_data = librosa.resample(data, sample_rate, new_sample_rate)
            output_file = join(output_path, filename)
            sf.write(output_file, new_data, new_sample_rate)
        except:
            print('Error converting ' + wavfile_path)
            return False

    return True


def get_transcript(wavefile_path):
    """
    Custom function to access a service STT. You must adapt it to use your contracted STT service.
        parameters:
            wavefile_path: wav filepath which will be transcribed.

        Returns:
            Text (str): Transcription of wav file.
    """
    files_data = {'file': open(wavefile_path, 'rb')}
    try:
        res = requests.post(url='https://YOU_URL_API',

                        files=files_data)
        res.encoding='utf-8'
    except KeyboardInterrupt:
        print("KeyboardInterrupt Detected!")
        exit()
    except:
        return False
    return res.text

def transcribe_audios(input_path, output_file):
    """
    Iterate over the wav files inside a folder and transcribe them all.
        parameters:
            input_path: input wavs folder.
            output_file: output file to save the transcriptions following the template: "filename| transcription"

        Returns:
            Boolean: True or False.
    """
    with open(output_file, 'w') as out:
        for wavfile_path in tqdm(sorted(glob(input_path + "/*.wav"))):
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
                    exc_file = split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Transcribing error: ")
                    print(exc_type, exc_file, exc_tb.tb_lineno)
                
            out.write("{}|{}\n".format(str(filename),str(text)))
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--transcription_file', default='transcript.txt', help='Filename to save the transcripts')
    parser.add_argument('--input_dir', default='wavs', help='Directory of wav files')
    parser.add_argument('--temp_dir', default='wavs_16k', help='Directory to save wav files with sample rate (16k)')
    parser.add_argument('--new_sample_rate', default=16000, help='Sample rate used by the transcription api.')

    args = parser.parse_args()

    input_path = join(args.base_dir, args.input_dir)
    converted_wavs_temp_path = join(args.base_dir,args.temp_dir)
    output_file = join(args.base_dir,args.transcription_file)

    # Convert audio sample rate
    print('Converting wav files...')
    convert_audios_samplerate(input_path, converted_wavs_temp_path, args.new_sample_rate)

    # Transcribe all wavs files
    print('Transcribing...')
    transcribe_audios(converted_wavs_temp_path, output_file)


if __name__ == "__main__":
  main()
