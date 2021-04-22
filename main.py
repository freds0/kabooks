import argparse
import glob
import os
import subprocess
import tqdm
import shutil
from config import Config

# Verify if transcription has already been performed
def transcription_already_done(folder):
    # Files verification
    transcription_path = os.path.join(folder, Config.transcription_file)
    if (os.path.exists(transcription_path)):
        with open(transcription_path) as f:
            content_file1 = f.readlines()
    else:
        # File dont exists
        return False

    text_book_path = os.path.join(folder, Config.text_book)
    if (os.path.exists(text_book_path)):
        with open(text_book_path) as f:
            content_file2 = f.readlines()
    else:
        # File dont exists
        return False

    if (len(content_file1) == len(content_file2)):              
        # Files are complete, everything is ok!
        return True
    else:
        # File is not complete
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_dir', default='input', help='Input folder')
    parser.add_argument('--output_dir', default='output', help='Output folder')
    args = parser.parse_args()

    base_dir = args.base_dir

    folders = os.listdir(os.path.join(base_dir, args.input_dir))
    total = len(folders)
    i = 0
    for folder_path in sorted(glob.glob(os.path.join(base_dir, args.input_dir) + '/*/')):
        if not os.path.isdir(folder_path):
            continue
        i += 1
        print('############################################## Step {} / {} ##############################################'.format(i, total))
        input_path = folder_path
        folder_name = folder_path.split('/')[-1]
        output_path = os.path.join(args.base_dir, args.output_dir, folder_name)

        if not(os.path.exists(output_path)):
            os.makedirs(output_path)

        # Normalizing text files
        print('Normalizing text files...')
        for txt_filepath in tqdm.tqdm(sorted(glob.glob(input_path + '/*.txt'))):
            txt_filename = txt_filepath.split('/')[-1]
            output_file = os.path.join(output_path, txt_filename)
            command_line = "python text_normalization.py --base_dir {} --input_file {} --output_file {} --min_words {} --max_words {}".format(base_dir, txt_filepath, output_file, Config.min_words, Config.max_words)
            subprocess.call(command_line, shell=True)

        # Spliting txt files
        print('Syncronizing audio/txt files...')
        for txt_filepath in tqdm.tqdm(sorted(glob.glob(output_path + '/*.txt'))):
            filename = txt_filepath.split('/')[-1].replace('.txt', Config.file_input_format)
            audio_file = os.path.join(input_path, filename)
            json_filepath = txt_filepath.replace('.txt', '.json')
            command_line = "python create_text_parts.py --base_dir {} --audio_file {} --text_file {} --output_file {}".format(base_dir, audio_file, txt_filepath, json_filepath)
            subprocess.call(command_line, shell=True)

        # Spliting audio files
        print('Spliting audio files...')
        splited_audios_folder = []
        for index, audio_filepath in enumerate(tqdm.tqdm(sorted(glob.glob(input_path + '/*' + Config.file_input_format)))):
            foldername = audio_filepath.split('/')[-1].replace(Config.file_input_format, '')
            splited_audiofiles_dir = foldername
            output_dir = os.path.join(output_path, splited_audiofiles_dir)
            splited_audios_folder.append(output_dir)
            json_filename = audio_filepath.split('/')[-1].replace(Config.file_input_format, '.json')
            json_filepath = os.path.join(output_path, json_filename)
            command_line = "python split_audio.py --base_dir {} --audio_file {} --filename_base {} --json_file {} --output_dir {} --metadata_file {}" .format(base_dir, audio_filepath, foldername, json_filepath, output_dir, Config.text_book)
            subprocess.call(command_line, shell=True)

        to_transcribe_audios_folder = []
        # Converting audio files to wav PCM 16
        print('Converting audio files...')
        for index, input_folder in enumerate(splited_audios_folder):
            input_dir = input_folder
            output_dir = input_folder + Config.suffix_tmp_dir
            to_transcribe_audios_folder.append(output_dir)
            command_line = "python convert_audio_files.py --base_dir {} --input_dir {} --output_dir {} " .format(base_dir, input_dir, output_dir)
            subprocess.call(command_line, shell=True)

        # Transcripting audio files
        print('Transcripting audio files...')
        for index, input_folder in enumerate(to_transcribe_audios_folder):
            input_dir = input_folder
            output_dir = input_folder.replace(Config.suffix_tmp_dir, '')
            if transcription_already_done(os.path.join(base_dir, output_dir)):
                continue
            command_line = "python transcript_audios.py --base_dir {} --input_dir {} --output_dir {} --transcription_file {}" .format(base_dir, input_dir, output_dir, Config.transcription_file)
            subprocess.call(command_line, shell=True)

        # Delete temporary folders and wav files
        for tmp_folder in to_transcribe_audios_folder:
            shutil.rmtree(tmp_folder, ignore_errors=True)

        # Validating audio files
        print('Validating text/transcript files...')
        for index, input_folder in enumerate(splited_audios_folder):
            output_dir = input_folder
            metadata1 = os.path.join(input_folder, Config.text_book)
            metadata2 = os.path.join(input_folder, Config.transcription_file)
            command_line = "python validation.py --base_dir {} --metadata_text {} --metadata_transcript {} --output_dir {} --output_file {} --threshold {}" .format(base_dir, metadata1, metadata2, output_dir, Config.validation_file, Config.val_threshold)
            subprocess.call(command_line, shell=True)

if __name__ == "__main__":
    main()
