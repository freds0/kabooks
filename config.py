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

    # selection
    selection_file = 'selected.csv'
    min_similarity = -1.0 # Negative value indicates that this step will be ignored
