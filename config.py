class Config:
    base_dir = './'

    # split_audio.py configurations
    text_book = 'metadata.csv'
    file_input_format = '.wav'

    # text_normalization.py configuration
    min_words = 10
    max_words = 35

    # convert_audio_files.py configurations
    suffix_tmp_dir = '_tmp'

    # transcript_audios.py  configurations
    transcription_file = 'transcription.csv'

    # validation.py
    validation_file = 'validation.csv'
    val_threshold = 0.7
