import argparse
from tqdm import tqdm
from glob import glob
from os.path import basename, join
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import torchaudio
import torchaudio.transforms as T

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model(language_id):

    if language_id == 'sp':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"
    elif language_id == 'it':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-italian"
    elif language_id == 'ge':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-german"
    elif language_id == 'pl':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-polish"
    elif language_id == 'pt':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
    elif language_id == 'en':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
    elif language_id == 'du':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-dutch"
    elif language_id == 'fr':
        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-french"

    processor = Wav2Vec2Processor.from_pretrained(model_id)
    model = Wav2Vec2ForCTC.from_pretrained(model_id)

    return processor, model.to(device)


def speech_file_to_array_fn(filepath, target_sample_rate=16000):

    filename = basename(filepath)
    waveform, sample_rate = torchaudio.load(filepath)
    if sample_rate != target_sample_rate:
        resampler = T.Resample(sample_rate, target_sample_rate)
        waveform = resampler(waveform)

    return waveform


def transcribe(processor, model, input_filepath, output_filepath):

    ofile = open(output_filepath, 'a')

    filename = basename(input_filepath)
    waveform = speech_file_to_array_fn(input_filepath, 16000)
    input_values = torch.tensor(waveform, device=device)

    with torch.no_grad():
        logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)

    line = "{}|{}".format(filename, transcription[0])
    ofile.write(line + "\n")

    ofile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_dir', default='./output/wavs', help='Wavs folder')
    parser.add_argument('--output_file', default='./output/transcription.csv', help='Name of csv output file')      
    parser.add_argument('--language', default='pt', help='du, en, fr, ge, it, pl, pt')
    args = parser.parse_args()

    processor, model = load_model(args.language)
    output_filepath = join(args.base_dir, args.output_file)
    ofile = open(output_filepath, 'w')
    ofile.close()

    for filepath in tqdm(sorted(glob(join(args.base_dir, args.input_dir) + '/*.wav'))):
        transcribe(processor, model, filepath, output_filepath)


if __name__ == "__main__":
    main()
