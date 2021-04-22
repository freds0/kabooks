#!/usr/bin/env python
# coding=utf-8
import argparse
import os
import json
from pydub import AudioSegment

#############################################################
# Linked segments lists
#############################################################
class Segment:
    def __init__(self, begin, end, text):
        self.begin = begin
        self.end = end
        self.text = text
        self.next = None
        self.filename = None
        self.gap = 0 # gap between segments (current and next)

    def set_next(self, next):
        self.next = next
        self.gap = next.begin - self.end

    def set_filename_and_id(self, filename, id):
        self.filename = filename
        self.id = id

    def merge_from(self, next):
        # merge two segments (current and next)
        self.next = next.next
        self.gap = next.gap
        self.end = next.end

    def duration(self, sample_rate):
        return (self.end - self.start - 1) / sample_rate


def read_json(json_path):

    head = None
    with  open(json_path) as jfile :
        data = json.load(jfile)
        for i, fragment in enumerate(data['fragments']):
            text = fragment['lines']
            begin = float(fragment['begin'])*1000
            end = float(fragment['end'])*1000

            # Build a segment list
            segment = Segment(begin, end, text)
            if head is None:
                head = segment
            else:
                prev.set_next(segment)
            prev = segment

    return head

def create_audio_segments(audio_file, filenames_base, head_list, output_dir):
    sound = AudioSegment.from_file(audio_file)
    curr = head_list
    i = 1
    while curr is not None:
        begin = curr.begin
        end = curr.end
        text = curr.text
        audio_segment = sound[begin:end]
        #filename = '{}-{:04d}.mp3'.format(filenames_base, i)
        filename = '{}-{:04d}.wav'.format(filenames_base, i)
        curr.set_filename_and_id(filename, i)
        filepath = os.path.join(output_dir, filename)
        #audio_segment.export(filepath)
        audio_segment.export(filepath, 'wav') 
        curr = curr.next
        i += 1
    return head_list

def create_metadata(head_list, output_file):
    separator = '|'
    curr = head_list
    with open(output_file, "w") as f:
        while curr is not None:
            text = curr.text
            filename = curr.filename.replace('.mp3', '')
            f.write(filename + separator + text[0] + '\n')
            curr = curr.next

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--audio_file', default='audio.mp3', help='Filename to input audio file')
    parser.add_argument('--filename_base', default='audio.mp3', help='Filename base of splited audios file')
    parser.add_argument('--json_file', default='output.json', help='Filename of input json file')
    parser.add_argument('--output_dir', default='output', help='Output dir')
    parser.add_argument('--metadata_file', default='metadata.csv', help='Filename to metadata output file')
    args = parser.parse_args()

    audio_path = os.path.join(args.base_dir, args.audio_file)
    json_path = os.path.join(args.base_dir, args.json_file)
    output_path = os.path.join(args.base_dir, args.output_dir)
    metadata_output_file = os.path.join(output_path, args.metadata_file)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    segments_list = read_json(json_path)
    segments_list = create_audio_segments(audio_path, args.filename_base, segments_list, output_path)
    create_metadata(segments_list, metadata_output_file)

if __name__ == "__main__":
    main()
