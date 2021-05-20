class Config:
    base_dir = './'

    # audio_segmentation.py configurations
    text_book = 'metadata.csv'
    file_input_format = '.wav'

    # text_normalization configuration
    min_words = 10
    max_words = 35

    # convert_audio_files configurations
    suffix_tmp_dir = '_tmp'
    sample_rate_tmp = 16000

    # transcribe configurations
    transcription_file = 'transcription.csv'

    # validation
    validation_file = 'validation.csv'
    val_threshold = 0.9
