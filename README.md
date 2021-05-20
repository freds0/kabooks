# KABooks - KABooks Audiobook dataset creator

KABOOKS is a tool to automate the process of creating datasets for training Text-To-Speech (TTS) and Speech-To-Text (STT) models.

Receiving an audio file and the corresponding text as input, KABooks will clean the text, dividing it into sentences, then use the external tool AENEAS to align the text with the audio. From this alignment, KABooks will segment the audio, according to the sentences created.

Finally, a validation step can be performed. For this, KABooks must use an external translation tool STT (not available here). This validation will calculate the similarity between the sentence and the transcript, using the Levenshtein distance. This step ensures that the text is correct. KABooks ccan be configured to perform a last selection step, in which will be discard audios that do not have a minimum guarantee of similarity between the sentence and the transcript.

Use at your own risk.

![kabooks-process](imgs/kabooks-process.png)

## Cleaning and Normalization of the text

In this step, a function is used that receives a raw text file, and performs its cleaning and normalization, dividing it into sentences. This function receives a maximum and minimum number of words that each sentence must contain. The function will try to split the sentences following these limits, but will not limit it strictly. This functionality is provided by the script named "text_normalization.py" and can be used separately.

## Align (Synchronization) Text-Audio 

For alignment, the AENEAS tool is used, which receives an audio file and the text (divided into sentences). A json file will be produced that contains the time (start and end) of each sentence in the text. Audio must be in wav or mp3 format. This functionality is provided by the script named "synchronization.py" and can be used separately.

## Audio Segmentation

This step receives the .json file from the previous step and performs the segmentation of the audio file. This script is based on the script provided by "Keith Ito", who kindly provided it via email. In this step, a logical list of segments is first created, storing the filename, the start and end times. Then, go through this logical list, dividing the original audio, saving each segment to disk. This functionality is provided by the script named "audio_segmentation.py" and can be used separately.

## Validate

Although the audio and text data are force-aligned with each other, several problems can happen that prejudices the results.
The text may be unclean or incorrect, the pronunciation may be erroneous or the audio may be corrupted (like ambient noise or poor recording quality).

KABooks can validate the text of the sentence. To do this, you must have available an external STT (not provided here), such as AWS, Google or Azure. Some sample scripts are available in the "tools" folder.  The external STT will generate a transcript of the segmented audio. So, you can compare the sentence with the transcript using the levenshtein distance, and thus have a guarantee that the audio really matches the text of the sentence.

This functionality is provided by the script named "validation.py" and can be used separately.

## Selection

After validating the data it is possible to select only those audios that have a minimal similarity between the transcription and the sentence. KABooks can discard audios that have a similarity value less than a value you define (90% is a good start).

This functionality is provided by the script named "selection.py" and can be used separately.

### How to create a docker image
```sh
$ git clone https://github.com/freds0/kabooks
$ cd kabooks
$ docker build -t kabooks ./
$ sudo docker run --rm --net='host' -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -v ~/:/root/ -w /root -it  kabooks
```

If you prefer use conda env:
```sh
$ conda create -n kabooks python=3.6 pip
$ conda activate kabooks
```

### Aeneas Installation
Requisites:
```sh
$ apt-get install ffmpeg espeak libespeak-dev wget git
$ wget https://raw.githubusercontent.com/readbeyond/aeneas/master/install_dependencies.sh
$ bash install_dependencies.sh
```
Installation:
```sh
$ git clone https://github.com/ReadBeyond/aeneas.git
$ cd aeneas
$ sudo pip install -r requirements.txt
$ python setup.py build_ext --inplace
$ python aeneas_check_setup.py
$ cd ..
$ pip install -e aeneas
```
### KABooks Installation

Install the requisites:

```sh
$ pip install -r requirements.txt
```
# Configuration

First, insert the mp3 (or wav) and txt files, with the same name, in the directory:

```sh
ls ./input
input/my_audiobook/file1.wav
input/my_audiobook/file1.txt
input/my_audiobook/file2.wav
input/my_audiobook/file2.txt
```

The result will be available in the folder::

```sh
ls ./output
output/my_audiobook/file1/
output/my_audiobook/file2/
```

Second, you will need set the variables in the file config.py:

```sh
base_dir = './'

# split_audio.py configurations
text_book = 'metadata.csv'
file_input_format = '.wav'

# text_normalization.py configuration
min_words = 10   # approximate minimum number of words in each sentence
max_words = 35   # approximate maximum number of words in each sentence

# convert_audio_files.py configurations
suffix_tmp_dir = '_tmp' # temporary folder suffix to store the converted audio files. This folder will be removed after completing the process.

# transcript_audios.py  configurations
transcription_file = 'transcription.csv' # file in which the transcripts of the audio files will be stored.

# validation.py
validation_file = 'validation.csv' # resulting file after data validation. The levenshtein distance between the transcript and the text is used to validate the data.
val_threshold = 0.9 # threshold for separation of files considered validated and with error.
```

# Execution

python main.py