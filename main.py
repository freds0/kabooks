import argparse
from glob import glob
from os.path import join, exists, isdir, split, dirname
from os import listdir, makedirs
from tqdm import tqdm
from config import Config
from convertion_tools import convert_mp3_to_wav
from segment_tools import build_segments
from transcription_tools import transcribe_files
from search_substring_with_threads import search_substring

def execute_pileline(args):

    for audiobooks_folder in tqdm(glob(args.input + "/*")):

        if not isdir(audiobooks_folder):
            continue

        for audio_filepath in glob(audiobooks_folder + "/*.mp3"):
            txt_filepath = audio_filepath.replace(".mp3", ".txt")

            if not exists(txt_filepath):
                print("Error: file {} doesn't exist!".format(txt_filepath))
                continue

            output_audiobook = join(args.output, split(dirname(audio_filepath))[-1])
            input_audiobook = dirname(audio_filepath)
            print("Converting mp3 to wav... ")
            r = convert_mp3_to_wav(input_audiobook, output_audiobook, Config.sample_rate)
            if not r:
                print("Error: conversion did not go well.")
                continue

            input_wavs = output_audiobook
            output_segments = join(output_audiobook, "wavs")
            print("Building wav segments... ")
            r = build_segments(input_wavs, output_segments, sample_rate=24000, min_duration=3, max_duration=15, max_gap_duration=3, threshold=32, output_filename=False, output_filename_id=1)
            if not r:
                print("Error: segmentation did not go well.")
                continue

            print("Transcribing wav segments... ")
            output_transcript_filepath = join(output_audiobook, "transcription.csv")
            input_wav_segments = output_segments
            transcribe_files(input_wav_segments, output_transcript_filepath, language="pt")

            print("Searching substrings.. ")
            input_transcript_file = output_transcript_filepath
            complete_text_file = txt_filepath
            output_filepath = join(output_audiobook, "result_search.csv")
            search_substring(input_transcript_file, complete_text_file, output_filepath, search_type=args.search_type, language='pt', n_threads=10)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-i', '--input', default='input', help='Input folder')
    parser.add_argument('-c', '--config', default='config.json', help='Config file')
    parser.add_argument('-o', '--output', default='output', help='Output folder')
    args = parser.parse_args()
    execute_pileline(args)


if __name__ == "__main__":
    main()
