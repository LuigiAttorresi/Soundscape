import os
import librosa
from spleeter.separator import Separator
import numpy as np

hop_length = 256
frame_length = 512
THRESHOLD = 0.0001

def separate(audio_file_name):
    audio_folder = os.path.join('audio')
    selected_file = os.path.join(audio_folder, audio_file_name)

    audio,sr = librosa.load(selected_file, sr=16000)

    separator = Separator('spleeter:4stems-16kHz')
    separator.separate_to_file(selected_file, 'output')

    stems_folder = os.path.join('output', audio_file_name.split('.')[0])
    stem_vocals = os.path.join(stems_folder, 'vocals.wav')
    stem_other = os.path.join(stems_folder, 'other.wav')
    stem_drums = os.path.join(stems_folder, 'drums.wav')
    stem_bass = os.path.join(stems_folder, 'bass.wav')

def get_vocals_array(audio_file_name):
    stems_folder = os.path.join('output', audio_file_name.split('.')[0])
    stem_vocals = os.path.join(stems_folder, 'vocals.wav')
    vocals, _ = librosa.load(stem_vocals, sr=16000)
    vocals = vocals[np.newaxis, :]       # A ddsp serve così
    return vocals, stem_vocals       

# Da fare per tutti


def is_present(audio_array):
    audio_rms = librosa.feature.rms(audio_array, frame_length=frame_length, hop_length=hop_length, center=True)
    return np.mean(audio_rms) > THRESHOLD


#if (~vocals_present & ~bass_present & ~drums_present):
#print('The track needs to have at least a singing voice or a bass line or a drum pattern!')