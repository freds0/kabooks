# KABooks - KABooks Audiobooks dataset creator

KABooks is a recursive acronym for "KABooks AudioBooks dataset creator" which is a tool to automate the process of creating datasets for training Text-To-Speech (TTS) and Speech-To-Text (STT) models. It is based on the work of Pansori [https://arxiv.org/abs/1812.09798]. 

Receiving an audio file and the corresponding text as input, KABooks will clean the text, dividing it into sentences, transcribe each segment and find the ground truth text at the complete text book.

Use at your own risk.

# Installation

Make sure to have ffmpeg installed:
```sh
$ apt-get update
$ apt install ffmpeg
```

```sh
$ conda create -n kabooks python=3.9 pip
$ conda activate kabooks
```


## Requirements Installation

Install pytorch:

```sh
pip3 install torch torchvision torchaudio
```

Install the KABooks requirements:

```sh
$ pip install -r requirements.txt
```

## Audio Segmentation

This step receives the json file from the previous step and performs the segmentation of the audio file. This script is based on the script provided by [Keith Ito](https://keithito.com), who kindly provided it via email. In this step, a logical list of segments is first created, storing the filename, the start and end times. Then, go through this logical list, dividing the original audio, saving each segment to disk. 

This functionality is provided by the script named "audio_segmentation.py" and can be used separately. Run the script using as input argument the path of the audio file (mp3) to be segmented.

```sh
$ python segment_tools.py 
```

The input must be an mp3 file, which must be inside the input folder. After executing the script, the audio segments will be generated in the wavs folder, and the segments will have the same names as the original file.


## Transcribe

Here there is a script to use Wav2Vec2. This functionality is provided by the script named "transcribe_audios.py" and can be used separately. Run the script using as input argument of the input directory of wavs files, the transcription output file. For example:

```sh
$ python transcription_tools.py
```

The script's default input is the contents of the wavs folder. The result will be a .csv (transcription.csv) file containing the transcript of each of the audio files present in the wavs folder.

## Search Text

In this step, each transcript from the previous step will be compared with the full text referring to the input audiobook. For each transcript the script will return a sentence with the greatest similarity, which was found in the full text. 

The result will be a .csv (result.csv) containing the transcript, the original sentence and a similarity value, for each of the audio segments present in the wavs folder.

```sh
$ python search_substring.py
```

You can also use the same version of this script, but using threads:

```sh
$ python search_substring_with_threads.py --number_threads=16
```

# References:

- Pansori [sourcecode](https://github.com/yc9701/pansori)
- Pansori [paper](https://arxiv.org/abs/1812.09798)
- [KATube](https://github.com/freds0/katube), our similar tool, used to create dataset from Youtube.

# Thanks

- [Keith Ito](https://keithito.com)
