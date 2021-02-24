import ddsp
import ddsp.training
from ddsp.colab import colab_utils
from ddsp.colab.colab_utils import (auto_tune, detect_notes, fit_quantile_transform, get_tuning_factor, DEFAULT_SAMPLE_RATE)
import tensorflow.compat.v2 as tf
import tensorflow_datasets as tfds
import os.path
import pickle
import gin
import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
import librosa
import feature_extraction
from omnizart.drum import app as dapp

sample_rate =  DEFAULT_SAMPLE_RATE
ADJUST = True

# Helper Functions
def shift_ld(audio_features, ld_shift=0.0):
    """Shift loudness by a number of ocatves."""
    audio_features['loudness_db'] += ld_shift
    return audio_features

def shift_f0(audio_features, pitch_shift=0.0):
  """Shift f0 by a number of ocatves."""
  audio_features['f0_hz'] *= 2.0 ** (pitch_shift)
  audio_features['f0_hz'] = np.clip(audio_features['f0_hz'], 0.0, librosa.midi_to_hz(110.0))
  return audio_features

def resynth(audio, audio_parameters):
    audio_features, _ = feature_extraction.extract_features(audio)
    audio = audio[np.newaxis, :]
    gin_file = os.path.join(audio_parameters["dir"], 'operative_config-0.gin')
    
    # Load the dataset statistics.
    DATASET_STATS = None
    dataset_stats_file = os.path.join(audio_parameters["dir"], 'dataset_statistics.pkl')
    print(f'Loading dataset statistics from {dataset_stats_file}')

    try:
        if tf.io.gfile.exists(dataset_stats_file):
            with tf.io.gfile.GFile(dataset_stats_file, 'rb') as f:
                DATASET_STATS = pickle.load(f)
            
    except Exception as err:
        print('Loading dataset statistics from pickle failed: {}.'.format(err))

    # Parse gin config,
    with gin.unlock_config():
        gin.parse_config_file(gin_file, skip_unknown=True)

    # Assumes only one checkpoint in the folder, 'ckpt-[iter]`.
    ckpt_files = [f for f in tf.io.gfile.listdir(audio_parameters["dir"]) if 'ckpt' in f]
    ckpt_name = ckpt_files[0].split('.')[0]
    ckpt = os.path.join(audio_parameters["dir"], ckpt_name)

    # Ensure dimensions and sampling rates are equal
    time_steps_train = gin.query_parameter('DefaultPreprocessor.time_steps')
    n_samples_train = gin.query_parameter('Additive.n_samples')
    hop_size = int(n_samples_train / time_steps_train)

    time_steps = int(audio.shape[1] / hop_size)
    n_samples = time_steps * hop_size

    gin_params = [
        'Additive.n_samples = {}'.format(n_samples),
        'FilteredNoise.n_samples = {}'.format(n_samples),
        'DefaultPreprocessor.time_steps = {}'.format(time_steps),
        'oscillator_bank.use_angular_cumsum = True',  # Avoids cumsum accumulation errors.
    ]

    with gin.unlock_config():
        gin.parse_config(gin_params)

    # Trim all input vectors to correct lengths
    for key in ['f0_hz', 'f0_confidence', 'loudness_db']:
        audio_features[key] = audio_features[key][:time_steps]
        #audio_features['audio'] = audio_features['audio'][:, :n_samples]

    # Set up the model just to predict audio given new conditioning
    model = ddsp.training.models.Autoencoder()
    model.restore(ckpt)

    # Build model by running a batch through it.
    _ = model(audio_features, training=False)

    # Resynthesize 
    audio_features_mod = {k: v.copy() for k, v in audio_features.items()}

    mask_on = None

    if ADJUST and DATASET_STATS is not None:
        # Detect sections that are "on".
        mask_on, note_on_value = detect_notes(audio_features['loudness_db'], audio_features['f0_confidence'], audio_parameters["threshold"])

        if np.any(mask_on):
            # Shift the pitch register.
            target_mean_pitch = DATASET_STATS['mean_pitch']
            pitch = ddsp.core.hz_to_midi(audio_features['f0_hz'])
            mean_pitch = np.mean(pitch[mask_on])
            p_diff = target_mean_pitch - mean_pitch
            p_diff_octave = p_diff / 12.0
            round_fn = np.floor if p_diff_octave > 1.5 else np.ceil
            p_diff_octave = round_fn(p_diff_octave)
            audio_features_mod = shift_f0(audio_features_mod, p_diff_octave)

            # Quantile shift the note_on parts.
            _, loudness_norm = colab_utils.fit_quantile_transform(audio_features['loudness_db'], mask_on, inv_quantile=DATASET_STATS['quantile_transform'])

            # Turn down the note_off parts.
            mask_off = np.logical_not(mask_on)
            loudness_norm[mask_off] -=  audio_parameters["quiet"] * (1.0 - note_on_value[mask_off][:, np.newaxis])
            loudness_norm = np.reshape(loudness_norm, audio_features['loudness_db'].shape)

            audio_features_mod['loudness_db'] = loudness_norm

            '''
            # Auto-tune.
            if autotune:
                f0_midi = np.array(ddsp.core.hz_to_midi(audio_features_mod['f0_hz']))
                tuning_factor = get_tuning_factor(f0_midi, audio_features_mod['f0_confidence'], mask_on)
                f0_midi_at = auto_tune(f0_midi, tuning_factor, mask_on, amount=autotune)
                audio_features_mod['f0_hz'] = ddsp.core.midi_to_hz(f0_midi_at)
            '''

        else:
            print('\nSkipping auto-adjust (no notes detected or ADJUST box empty).')

    else:
        print('\nSkipping auto-adujst (box not checked or no dataset statistics found).')

    # Manual Shifts.
    audio_features_mod = shift_ld(audio_features_mod, audio_parameters["loudness_shift"])
    audio_features_mod = shift_f0(audio_features_mod, audio_parameters["pitch_shift"])

    af = audio_features if audio_features_mod is None else audio_features_mod

    # Run a batch of predictions.
    outputs = model(af, training=False)
    new_audio = model.get_audio_from_outputs(outputs)

    # Write new_audio into a file.
    # If batched, take first element.
    if len(new_audio.shape) == 2:
        new_audio = new_audio[0]

    normalizer = float(np.iinfo(np.int16).max)
    array_of_ints = np.array(
        np.asarray(new_audio) * normalizer, dtype=np.int16)
    filename = "generated_" + audio_parameters["type"] + ".wav"
    wavfile.write(filename, DEFAULT_SAMPLE_RATE, array_of_ints)

    return new_audio  # Or array_of_ints??

def drum_resynth(drum_audio_path, soundfont_path):

    # Omnizart Transcribe and Resynthesize
    print('Transcribing drums...')
    midi = dapp.transcribe(drum_audio_path, model_path=None)
    print('Drums transcribed!')

    print('Resynth drums...')
    # out_name = f"{uploaded_audio}_synth.wav"
    out_name = "generated_drums.wav"
    raw_wav = midi.fluidsynth(fs=44100, sf2_path=soundfont_path)
    wavfile.write(out_name, 44100, raw_wav)
    new_audio, sr = librosa.load(out_name, sr=16000)
    print('Drums Resynthesized!')
    return new_audio