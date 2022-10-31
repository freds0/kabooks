from os.path import isfile, isdir, basename, join
import urllib.request
import progressbar
import tarfile


class MyProgressBar():
    '''
    Progress Bar for Download. Source: https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
    '''
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def download_books_dataset(lang = 'pt'):
    '''
    Download Books information.
    '''
    url = 'https://dl.fbaipublicfiles.com/mls/lv_text.tar.gz'

    books_filename = url.split('/')[-1]

    if isfile(books_filename):
        print('File {} exists!'.format(books_filename))
        return books_filename

    try:
        urllib.request.urlretrieve(url, books_filename, MyProgressBar())
    except Exception as e:
        print(e)
        return False

    return books_filename

def download_language_dataset(lang = 'pt'):
    '''
    Download datasets
    '''

    # Choose dataset
    if lang == 'pt':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_portuguese_opus.tar.gz'
    elif lang == 'pl':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_polish_opus.tar.gz'
    elif lang == 'it':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_italian_opus.tar.gz'        
    elif lang == 'sp':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_spanish_opus.tar.gz'
    elif lang == 'fr':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_french_opus.tar.gz'
    elif lang == 'du':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_dutch_opus.tar.gz'
    elif lang == 'ge':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_german_opus.tar.gz'
    elif lang == 'en':
        url = 'https://dl.fbaipublicfiles.com/mls/mls_english_opus.tar.gz'
    else:
        print('Error: invalid language {}.'.format(lang))        
        return False

    transcripts_filename = url.split('/')[-1]
    if isfile(transcripts_filename):
        print('File {} exists!'.format(transcripts_filename))

    else:
        # Download transcripts information
        try:
            urllib.request.urlretrieve(url, transcripts_filename, MyProgressBar())
        except Exception as e:
            print(e)
            return False

    return transcripts_filename

def extract_transcript_files(tar_filename_transcripts):
    '''
    Extract transcripts.txt file from MLS tar.gz
    '''

    # Extract transcripts
    basefilename = basename(tar_filename_transcripts).split('.')[0]
    dev_trans_file   = join(basefilename, 'dev/transcripts.txt')
    test_trans_file  = join(basefilename, 'test/transcripts.txt')
    train_trans_file = join(basefilename, 'train/transcripts.txt')

    transcripts_files = [
        dev_trans_file,
        test_trans_file,
        train_trans_file
    ]

    if isfile(dev_trans_file) and isfile(test_trans_file) and isfile(train_trans_file):
        print('Transcripts already extracted!')
        return transcripts_files

    try:
        tar_file = tarfile.open(tar_filename_transcripts)
        tar_file.extract(dev_trans_file,'./')
        tar_file.extract(test_trans_file,'./')
        tar_file.extract(train_trans_file,'./')
        tar_file.close()
    except Exception as e:
        print(e)
        return False

    return transcripts_files


def extract_book_files(tar_filename_books):
    '''
    Extract book files
    '''
    basefilename  = basename(tar_filename_books).split('.')[0]

    if isdir(basefilename):
        print('File {} already extracted!'.format(basefilename))
        return basefilename
    try:
        tar_file = tarfile.open(tar_filename_books)
        tar_file.extractall()
        tar_file.close()
    except Exception as e:
        print(e)
        return False

    return basename

def extract_segment_files(tar_filename_segments):
    '''
    Extract segments.txt file from tar.gz
    '''
    basefilename   = basename(tar_filename_segments).split('.')[0]
    dev_file   = join(basefilename, 'dev/segments.txt')
    test_file  = join(basefilename, 'test/segments.txt')
    train_file = join(basefilename, 'train/segments.txt')

    segments_files = [
        dev_file,
        test_file,
        train_file
    ]

    if isfile(dev_file) and isfile(test_file) and isfile(train_file):
        print('Segments files exists!')
        return segments_files

    try:
        tar_file = tarfile.open(tar_filename_segments)
        tar_file.extract(dev_file,'./')
        tar_file.extract(test_file,'./')
        tar_file.extract(train_file,'./')
        tar_file.close()
    except Exception as e:
        print(e)
        return False

    return segments_files