#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Adapted from https://gist.github.com/keithito/771cfc1a1ab69d1957914e377e65b6bd from Keith Ito: kito@kito.us
#
import glob
import argparse
from os import listdir
from os.path import isfile, join
from collections import OrderedDict
import librosa
import numpy as np
import os
import sys
from scipy.io.wavfile import write

class Segment:
  '''
  Linked segments lists
  '''
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.next = None
    self.gap = 0 # gap between segments (current and next)

  def set_next(self, next):
    self.next = next
    self.gap = next.start - self.end

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


def segment_wav(wav, threshold_db):
  '''
  Segment audio file and return a segment linked list
  '''
  # Find gaps at a fine resolution:
  parts = librosa.effects.split(wav, top_db=threshold_db, frame_length=1024, hop_length=256)

  # Build up a linked list of segments:
  head = None
  for start, end in parts:
    segment = Segment(start, end)
    if head is None:
      head = segment
    else:
      prev.set_next(segment)
    prev = segment
  return head


def find_best_merge(segments, sample_rate, max_duration, max_gap_duration):
  '''
  Find small segments that can be merged by analyzing max_duration and max_gap_duration
  '''
  best = None
  best_score = 0
  s = segments
  while s.next is not None:
    gap_duration = s.gap / sample_rate
    merged_duration = (s.next.end - s.start) / sample_rate
    if gap_duration <= max_gap_duration and merged_duration <= max_duration:
      score = max_gap_duration - gap_duration
      if score > best_score:
        best = s
        best_score = score
    s = s.next
  return best


def find_segments(filename, wav, sample_rate, min_duration, max_duration, max_gap_duration, threshold_db):
  '''
  Given an audio file, creates the best possible segment list
  '''
  # Segment audio file
  segments = segment_wav(wav, threshold_db)
  # Merge until we can't merge any more
  while True:
    best = find_best_merge(segments, sample_rate, max_duration, max_gap_duration)
    if best is None:
      break
    best.merge_from(best.next)

  # Convert to list
  result = []
  s = segments
  while s is not None:
    result.append(s)
    # Create a errors file
    if (s.duration(sample_rate) < min_duration and
        s.duration(sample_rate) > max_duration):
        with open(os.path.join(os.path.dirname(__file__), "errors.txt"), "a") as f:
            f.write(filename+"\n")
    # Extend the end by 0.2 sec as we sometimes lose the ends of words ending in unvoiced sounds.
    s.end += int(0.2 * sample_rate)
    s = s.next

  return result


def load_filenames(input_dir):
  '''
  Given an folder, creates a wav file alphabetical order dict
  '''
  mappings = OrderedDict()
  for filepath in glob.glob(join(input_dir + "/*.wav")):
    filename = filepath.split('/')[-1].split('.')[0]
    mappings[filename] = filepath
  return mappings


def build_segments(input_dir, output_dir, sample_rate=24000, min_duration=3, max_duration=15, max_gap_duration=3, threshold=28, output_filename=False, output_filename_id=1):
  '''
  Build best segments of wav files
  '''
  # Creates destination folder
  os.makedirs(output_dir, exist_ok=True)
  # Initializes variables
  segment_max_duration, mean_duration = 0, 0
  all_segments = []
  total_duration = 0
  filenames = load_filenames(input_dir)
  for i, (file_id, filename) in enumerate(filenames.items()):
    print('Loading %s: %s (%d of %d)' % (file_id, filename, i+1, len(filenames)))
    wav, sample_rate = librosa.load(filename, sr=sample_rate)
    print(' -> Loaded %.1f min of audio. Splitting...' % (len(wav) / sample_rate / 60))

    # Find best segments
    segments = find_segments(filename, wav, sample_rate, min_duration, max_duration, max_gap_duration, threshold)
    duration = sum((s.duration(sample_rate) for s in segments))
    total_duration += duration

    # Create records for the segments
    output_filename = output_filename  if output_filename else file_id
    j = int(output_filename_id)
    for s in segments:
      all_segments.append(s)
      s.set_filename_and_id(filename, '%s-%04d' % (output_filename, j))
      j = j + 1

    print(' -> Segmented into %d parts (%.1f min, %.2f sec avg)' % (
      len(segments), duration / 60, duration / len(segments)))

    # Write segments to disk:
    for s in segments:
      #segment_wav = (wav[s.start:s.end] * 32767).astype(np.int16)
      segment_wav = (wav[s.start:s.end] * 32767).astype(np.int16)
      out_path = os.path.join(output_dir, '%s.wav' % s.id)
      #librosa.output.write_wav(out_path, segment_wav, sample_rate)
      write(out_path, sample_rate, segment_wav)

      duration += len(segment_wav) / sample_rate
      duration_segment = len(segment_wav) / sample_rate
      if duration_segment > segment_max_duration:
        segment_max_duration = duration_segment

      mean_duration = mean_duration + duration_segment
    print(' -> Wrote %d segment wav files' % len(segments))
    print(' -> Progress: %d segments, %.2f hours, %.2f sec avg' % (
      len(all_segments), total_duration / 3600, total_duration / len(all_segments)))

  print('Writing metadata for %d segments (%.2f hours)' % (len(all_segments), total_duration / 3600))
  with open(os.path.join(output_dir, 'segments.csv'), 'w') as f:
    for s in all_segments:
      f.write('%s|%s|%d|%d\n' % (s.id, s.filename, s.start, s.end))
  print('Mean: %f' %( mean_duration / len(segments) ))
  print('Max: %d' %(segment_max_duration ))
  return True


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--base_dir', default='./')
  parser.add_argument('-i', '--input', default='./input', help='Name of the origin wav folder')
  parser.add_argument('-o', '--output', default='./output/wavs', help='Name of wav folder')
  parser.add_argument('--min_duration', type=float, default=3.0, help='In seconds')
  parser.add_argument('--max_duration', type=float, default=15.0, help='In seconds')
  parser.add_argument('--max_gap_duration', type=float, default=3.0, help='In seconds')
  parser.add_argument('--sample_rate', type=int, default=24000, help='Sampling rate')
  parser.add_argument('--output_filename', type=str, default='', help='')
  parser.add_argument('--output_filename_id', type=int, default=1, help='Sequencial number used for id filename.')
  parser.add_argument('--threshold', type=float, default=28.0, help='The threshold (in decibels) below reference to consider as silence')
  args = parser.parse_args()

  input_filepath = join(args.base_dir, args.input)
  output_dir = join(args.base_dir, args.output)
  build_segments(input_filepath, 
                 output_dir, 
                 args.sample_rate, 
                 args.min_duration, 
                 args.max_duration,
                 args.max_gap_duration, 
                 args.threshold, 
                 args.output_filename, 
                 args.output_filename_id
  )


if __name__ == "__main__":
  main()
