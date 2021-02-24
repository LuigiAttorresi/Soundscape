print('Start separate input')

import os
import librosa
from spleeter.separator import Separator
import numpy as np

print('End separate input')


hop_length = 256
frame_length = 512
THRESHOLD = 0.0001
stems_names = {
    'vocals': 'vocals.wav', 
    'bass': 'bass.wav', 
    'drums': 'drums.wav', 
    'other': 'other.wav'}

def separate(audio_file_name):
    audio_folder = os.path.join('audio')
    selected_file = os.path.join(audio_folder, audio_file_name)

    audio, _ = librosa.load(selected_file, sr=16000)

    separator = Separator('spleeter:4stems-16kHz')
    separator.separate_to_file(selected_file, 'output')

def get_stem_array(audio_file_name, stem_type):
    stems_folder = os.path.join('output', audio_file_name.split('.')[0])
    stem = os.path.join(stems_folder, stems_names[stem_type])
    audio, _ = librosa.load(stem, sr=16000)
    return audio, stem  

def is_present(audio_array):
    audio_rms = librosa.feature.rms(audio_array, frame_length=frame_length, hop_length=hop_length, center=True)
    return np.mean(audio_rms) > THRESHOLD