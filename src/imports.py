###############
### IMPORTS ###
###############

print('Starting imports...')

import os
import os.path
#from IPython import display as dsp  #Togliere?

import warnings
warnings.filterwarnings("ignore")

import copy

import crepe
import ddsp
import ddsp.training

''' PER PYTHONANYWHERE
!sudo apt-get install libportaudio2 #In pythonanywhere potrebbe non servire (bug sounddevice)
!pip install sounddevice
import sounddevice as sd
from scipy.io.wavfile import write
(servono a registrare e riprodurre)
'''
''' Per evitare gli import
from ddsp.colab.colab_utils import (
    play, record,
    upload)

from ddsp.colab import colab_utils

from ddsp.colab.colab_utils import (
    auto_tune, detect_notes, fit_quantile_transform,
    get_tuning_factor, download, play, record,
    specplot, upload, DEFAULT_SAMPLE_RATE)
'''
import gin
#from google.colab import files
import librosa
#import matplotlib.pyplot as plt   #Togliere?
import numpy as np
import pickle
import tensorflow.compat.v2 as tf
import tensorflow_datasets as tfds

# Helper Functions
sample_rate = 16000

#from IPython.display import Audio   #Togliere?
from scipy.io.wavfile import write
#import IPython.display as ipd     #Togliere?
from pathlib import Path
from random import randrange

import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf

import base64
import io

from IPython import display #Serve per play
import note_seq
from scipy import stats
from scipy.io import wavfile

from spleeter.separator import Separator

from omnizart.drum import app as dapp

import scipy.io.wavfile as wave

from ddsp.colab import colab_utils
print('Imports done!')