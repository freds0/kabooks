#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import glob
from os import makedirs
from os.path import isfile, join, basename
from pydub import AudioSegment
import pydub

def convert_mp3_to_wav(input, output, sample_rate):

    makedirs(output, exist_ok=True)

    for input_file in glob.glob(input + '/*.mp3'):
        filename = basename(input_file).split('.')[0]
        output_file = join(output, filename + '.wav')
        command_line = "ffmpeg -i {} -ar {}  {}" .format(input_file, int(sample_rate), output_file)

        r = subprocess.call(command_line, shell=True)
        if r != 0:
            return False

        return True
       

def convert_mp3_to_wav_with_pydub(input, output, sample_rate):
    '''
    Convert mp3 folder files to wav
    '''
    for input_file in glob.glob(input + '/*.mp3'):
        filename = basename(input_file).split('.')[0]
        output_file = join(output, filename + '.wav')
        #sound = AudioSegment.from_file(input_file, format="mp3")
        sound = AudioSegment.from_mp3(input_file)
        sound.export(output_file, format="wav")


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--base_dir', default='./')
  parser.add_argument('-i', '--input', default='input', help='Input folder')
  parser.add_argument('-o', '--output', default='output', help='Output folder')
  parser.add_argument('-s', '--sample_rate', default=24000, help='Output sampling rate')
  args = parser.parse_args()

  output = join(args.base_dir, args.output)
  input = join(args.base_dir,args.input)
  convert_mp3_to_wav(input, output, args.sample_rate)


if __name__ == "__main__":
  main()

