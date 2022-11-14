!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import glob
from os import makedirs
from os.path import isfile, join, basename

def convert(args):

    makedirs(join(args.base_dir,args.output), exist_ok=True)  
    input_dir = join(args.base_dir,args.input)

    for input_file in glob.glob(input_dir + '/*.mp3'):
        filename = basename(input_file).split('.')[0]
        output_file = join(args.base_dir, args.output, filename + '.wav')
        command_line = "ffmpeg -i {} -ar {}  {}" .format(input_file, int(args.sample_rate), output_file)  
        subprocess.call(command_line, shell=True)
       

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--base_dir', default='./')
  parser.add_argument('-i', '--input', default='input', help='Input folder')
  parser.add_argument('-o', '--output', default='output', help='Output folder')
  parser.add_argument('-s', '--sample_rate', default=16000, help='Output sampling rate')
  args = parser.parse_args()
  convert(args)


if __name__ == "__main__":
  main()

