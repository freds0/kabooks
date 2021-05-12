import argparse
from glob import glob
from os.path import join, exists, isdir
from os import listdir, makedirs
from tqdm import tqdm
import shutil
from config import Config
from text_normalization import create_normalized_text_from_subtitles_file
from synchronization import create_aeneas_json_file
from audio_segmentation import segment_audio
from transcribe import convert_audios_samplerate, transcribe_audios
from validation import create_validation_file


# Verify if transcription has already been performed
def transcription_already_done(folder):
    # Files verification
    transcription_path = join(folder, Config.transcription_file)
    if exists(transcription_path):
        with open(transcription_path) as f:
            content_file1 = f.readlines()
    else:
        # File dont exists
        return False

    text_book_path = join(folder, Config.text_book)
    if exists(text_book_path):
        with open(text_book_path) as f:
            content_file2 = f.readlines()
    else:
        # File dont exists
        return False

    if len(content_file1) == len(content_file2):
        # Files are complete, everything is ok!
        return True
    else:
        # File is not complete
        return False


def execute(args):
    folders = listdir(join(args.base_dir, args.input_dir))
    total = len(folders)
    i = 0
    for folder_path in sorted(glob(join(args.base_dir, args.input_dir) + '/*/')):
        if not isdir(folder_path):
            continue
        i += 1
        print('############################################## Step {} / {} ##############################################'.format(i, total))
        input_path = folder_path
        folder_name = folder_path.split('/')[-1]
        output_path = join(args.base_dir, args.output_dir, folder_name)

        if not(exists(output_path)):
            makedirs(output_path)

        # Normalizing text files
        print('Normalizing text files...')
        for txt_filepath in tqdm(sorted(glob(input_path + '/*.txt'))):
            txt_filename = txt_filepath.split('/')[-1]
            output_file = join(output_path, txt_filename)

            create_normalized_text_from_subtitles_file(subtitle_file=txt_filepath, output_file=output_file, min_words=Config.min_words, max_words=Config.max_words)

        exit()
        # Spliting txt files
        print('Syncronizing audio/txt files...')
        for txt_filepath in tqdm(sorted(glob(output_path + '/*.txt'))):
            filename = txt_filepath.split('/')[-1].replace('.txt', Config.file_input_format)
            audio_file = join(input_path, filename)
            json_filepath = txt_filepath.replace('.txt', '.json')

            create_aeneas_json_file(audio_path=audio_file, text_path=txt_filepath, output_path=json_filepath)

        # Spliting audio files
        print('Spliting audio files...')
        splited_audios_folder = []
        for index, audio_filepath in enumerate(tqdm(sorted(glob(input_path + '/*' + Config.file_input_format)))):
            foldername = audio_filepath.split('/')[-1].replace(Config.file_input_format, '')
            output_dir = join(output_path, foldername)
            splited_audios_folder.append(output_dir)
            json_filename = audio_filepath.split('/')[-1].replace(Config.file_input_format, '.json')
            json_filepath = join(output_path, json_filename)
            metadata_output_file = join(args.base_dir, output_dir, Config.text_book)

            segment_audio(audio_path=audio_filepath, json_path=json_filepath, output_path=output_dir, metadata_output_file=metadata_output_file, filename_base=foldername)

        to_transcribe_audios_folder = []
        # Converting audio files to wav PCM 16
        print('Converting audio files...')
        for index, input_folder in enumerate(splited_audios_folder):
            input_dir = input_folder
            output_dir = input_folder + Config.suffix_tmp_dir
            to_transcribe_audios_folder.append(output_dir)

            convert_audios_samplerate(input_path=input_dir, output_path=output_dir, new_sample_rate=Config.sample_rate_tmp)

        # Transcribing audio files
        print('Transcribing audio files...')
        for index, input_folder in enumerate(to_transcribe_audios_folder):
            output_dir = input_folder.replace(Config.suffix_tmp_dir, '')
            output_filepath = join(output_dir, Config.transcription_file)
            if transcription_already_done(join(args.base_dir, output_dir)):
                continue

            transcribe_audios(input_path=input_folder, output_file=output_filepath)

        # Delete temporary folders and wav files
        for tmp_folder in to_transcribe_audios_folder:
            shutil.rmtree(tmp_folder, ignore_errors=True)

        # Validating audio files
        print('Validating text/transcript files...')
        for index, input_folder in enumerate(splited_audios_folder):
            output_dir = input_folder
            metadata1 = join(input_folder, Config.text_book)
            metadata2 = join(input_folder, Config.transcription_file)
            output_filepath = join(input_folder, Config.validation_file)
            create_validation_file(input_file1=metadata1, input_file2=metadata2, prefix_filepath=output_dir, output_file=output_filepath)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_dir', default='input', help='Input folder')
    parser.add_argument('--output_dir', default='output', help='Output folder')
    args = parser.parse_args()
    execute(args)


if __name__ == "__main__":
    main()
