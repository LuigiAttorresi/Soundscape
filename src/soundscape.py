
from imports import * 


# Helper Functions
def shift_ld(audio_features, ld_shift=0.0):
    """Shift loudness by a number of ocatves."""
    audio_features['loudness_db'] += ld_shift
    return audio_features
    #
    #
def shift_f0(audio_features, pitch_shift=0.0):
  """Shift f0 by a number of ocatves."""
  audio_features['f0_hz'] *= 2.0 ** (pitch_shift)
  audio_features['f0_hz'] = np.clip(audio_features['f0_hz'], 0.0, librosa.midi_to_hz(110.0))
  return audio_features

### recording functions

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def rec_and_save():
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument(
	    '-l', '--list-devices', action='store_true',
	    help='show list of audio devices and exit')
	args, remaining = parser.parse_known_args()
	if args.list_devices:
	    print(sd.query_devices())
	    parser.exit(0)
	parser = argparse.ArgumentParser(
	    description=__doc__,
	    formatter_class=argparse.RawDescriptionHelpFormatter,
	    parents=[parser])
	parser.add_argument(
	    'filename', nargs='?', metavar='FILENAME',
	    help='audio file to store recording to')
	parser.add_argument(
	    '-d', '--device', type=int_or_str,
	    help='input device (numeric ID or substring)')
	parser.add_argument(
	    '-r', '--samplerate', type=int, help='sampling rate')
	parser.add_argument(
	    '-c', '--channels', type=int, default=1, help='number of input channels')
	parser.add_argument(
	    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
	args = parser.parse_args(remaining)

	q = queue.Queue()

	def callback(indata, frames, time, status):
	    if status:
	        print(status, file=sys.stderr)
	    q.put(indata.copy())


	try:
	    if args.samplerate is None:
	        device_info = sd.query_devices(args.device, 'input')
	        # soundfile expects an int, sounddevice provides a float:
	        args.samplerate = int(device_info['default_samplerate'])
	    if args.filename is None:
		    args.filename = os.path.join('audio', 'recording.wav')

	    # Make sure the file is opened before recording anything:
	    with sf.SoundFile(args.filename, mode='w', samplerate=args.samplerate,
	                      channels=args.channels, subtype=args.subtype) as file:
	        with sd.InputStream(samplerate=args.samplerate, device=args.device,
	                            channels=args.channels, callback=callback):
	            print('#' * 80)
	            print('press Ctrl+C to stop the recording')
	            print('#' * 80)
	            while True:
	                file.write(q.get())
	except KeyboardInterrupt:
	    print('\nRecording finished: ' + repr(args.filename))
	except Exception as e:
	    parser.exit(type(e).__name__ + ': ' + str(e))
      
print('Initialization Done!')


############
### MAIN ###
############

if __name__ == "__main__":
  # Using embedded configuration.

  print('Registra audio con microfono (m) o usare brano di prova (p)?')
  input_type = input()
  audio_folder = os.path.join('audio')
  audio_file_name = 'celeste.wav' #TODO: implement selection

  if(input_type == 'm'):
    rec_and_save()
    audio_file_name = 'recording.wav'


  selected_file = os.path.join(audio_folder, audio_file_name)

  separator = Separator('spleeter:4stems-16kHz')
  separator.separate_to_file(selected_file, 'output')

  #write("Brani Prova\Fly Me - Cut.wav", 16000, audio.T)

  stems_folder = os.path.join('output', audio_file_name.split('.')[0])
  stem_vocals = os.path.join(stems_folder, 'vocals.wav')
  stem_other = os.path.join(stems_folder, 'other.wav')
  stem_drums = os.path.join(stems_folder, 'drums.wav')
  stem_bass = os.path.join(stems_folder, 'bass.wav')

  vocals, sr = librosa.load(stem_vocals, sr=16000)
  other, sr = librosa.load(stem_other, sr=16000)
  drums, sr = librosa.load(stem_drums, sr=16000)
  bass, sr = librosa.load(stem_bass, sr=16000)

  #Serve solo per i modelli armonici
  hop_length = 256
  frame_length = 512
  vocals_rms = librosa.feature.rms(vocals, frame_length=frame_length, hop_length=hop_length, center=True)
  drums_rms = librosa.feature.rms(drums, frame_length=frame_length, hop_length=hop_length, center=True)
  bass_rms = librosa.feature.rms(bass, frame_length=frame_length, hop_length=hop_length, center=True)

  THRESHOLD = 0.0001

  vocals_present = np.mean(vocals_rms) > THRESHOLD
  bass_present = np.mean(bass_rms) > THRESHOLD
  drums_present = np.mean(drums_rms) > THRESHOLD

  if vocals_present:
    vocals = vocals[np.newaxis, :]
    print('The track contains vocals')
  if bass_present:
    print('The track contains bass')
    bass = bass[np.newaxis, :]
  if drums_present:
    print('The track contains drums')
  if (~vocals_present & ~bass_present & ~drums_present):
    print('The track needs to have at least a singing voice or a bass line or a drum pattern!')

  # # %% 
  # Setup the session.
  ddsp.spectral_ops.reset_crepe()
  
  # # Compute features.
  print("extracting features")
  #import time
  #start_time = time.time()

  if vocals_present:
    vocals_features = ddsp.training.metrics.compute_audio_features(vocals)
    vocals_features['loudness_db'] = vocals_features['loudness_db'].astype(np.float32)
    vocals_features_mod = None

  if bass_present:
    bass_features = ddsp.training.metrics.compute_audio_features(bass)
    bass_features['loudness_db'] = bass_features['loudness_db'].astype(np.float32)
    bass_features_mod = None
  
  #print('Audio features took %.1f seconds' % (time.time() - start_time))

  TRIM = -15
  
  # # %%
  # #Choose the sound for vocals
  
  # ''' DA FARE
  # - Dare la possibilità all'utente di scegliere il soundscape. Sulla base di quello e
  # delle energie dei segnali ad ogni traccia viene assegnato un modello e rispettivi
  # parametri di loudness e pitch shift
  
  # - Gestire i file dei modelli
  # '''
  
  #model = 'BarcaTD 30K' #@param ['Anatra 10K', 'Anatra 20K', 'Anatra 30K Sbagliata', 'Anatra 30K', 'Anatra 40K', 'Motosega 10K', 'Lupo 30K', 'Barca 22K', 'Barca 30K', 'Barca 40K', 'Locomotiva 22K', 'Locomotiva 30K', 'Locomotiva 40K', 'Foca 20K', 'Foca 30K', 'Foca 40K', 'Rana 20K', 'Rana 30K', 'Mosca 8K', 'Mosca 12K', 'Mosca 20K', 'Mosca 30K', 'Gabbiano 20K', 'Gabbiano 30K', 'Gabbiano 40K', 'Treno 20K', 'Treno 30K', 'Treno 40K', 'Mucca 24K', 'Mucca 30K', 'Mucca 40K', 'BarcaTD 16K', 'BarcaTD 20K', 'BarcaTD 30K', 'BarcaTD 40K']
  #MODEL = model
  
  # Harmonic part
  
  # Funzione NON NECESSARIA (?)
  # def find_model_dir(dir_name):
  #   # Iterate through directories until model directory is found
  #   for root, dirs, filenames in os.walk(dir_name):
  #     for filename in filenames:
  #       if filename.endswith(".gin") and not filename.startswith("."):
  #         model_dir = root
  #         break
  #   return model_dir
  
  # model_dir = find_model_dir('models/Anatra40K')

  # ''' PER DOPO
  # if model == 'Anatra 10K':
  #   #FOLEY_PATH = '/content/drive/MyDrive/Prototipo_CPAC/Forest/Forest_foley/'
  #   model_dir = find_model_dir('/content/drive/MyDrive/Soundscapes014/Anatra10K')
  #   #BACKGROUND_PATH = '/content/drive/MyDrive/Prototipo_CPAC/Forest/Background/snow_forest.wav'
  #   #mix = 0.9
  #   #pitch_shift = 0
  # '''


  soundscape = 'Stagno'

  ADJUST = True

  if soundscape == 'Stagno':
    # VOCALS
    vocals_dir = 'models/Anatra40K'
    vocals_threshold = 1
    vocals_quiet = 20
    vocals_autotune = 0
    vocals_loudness_shift = 0
    vocals_pitch_shift = 0

    # BASS
    bass_dir = 'models/Mosca12K'
    bass_threshold = 1
    bass_quiet = 20
    bas_autotune = 0
    bass_loudness_shift = 0
    bass_pitch_shift = 0

        
  elif soundscape == 'Montagna':
    # VOCALS
    vocals_dir = 'models/Motosega10K'
    vocals_threshold = 1
    vocals_quiet = 20
    vocals_autotune = 0
    vocals_loudness_shift = 0
    vocals_pitch_shift = 0

    # BASS
    bass_dir = 'models/Mucca40K'
    bass_threshold = 1
    bass_quiet = 20
    bas_autotune = 0
    bass_loudness_shift = 0
    bass_pitch_shift = -1


  elif soundscape == 'Mare':
    # VOCALS
    vocals_dir = 'models/Gabbiano40K'
    vocals_threshold = 1
    vocals_quiet = 20
    vocals_autotune = 0
    vocals_loudness_shift = 0
    vocals_pitch_shift = 0

    # BASS
    bass_dir = 'models\Barca40K'
    bass_threshold = 1
    bass_quiet = 20
    bas_autotune = 0
    bass_loudness_shift = 0
    bass_pitch_shift = -1

  # VOCALS RESYNTHESIS

  if vocals_present:
    
    gin_file = os.path.join(vocals_dir, 'operative_config-0.gin')
    
    
    # Load the dataset statistics.
    DATASET_STATS = None
    dataset_stats_file = os.path.join(vocals_dir, 'dataset_statistics.pkl')
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
    ckpt_files = [f for f in tf.io.gfile.listdir(vocals_dir) if 'ckpt' in f]
    ckpt_name = ckpt_files[0].split('.')[0]
    ckpt = os.path.join(vocals_dir, ckpt_name)
    
    # # Ensure dimensions and sampling rates are equal
    time_steps_train = gin.query_parameter('DefaultPreprocessor.time_steps')
    n_samples_train = gin.query_parameter('Additive.n_samples')
    hop_size = int(n_samples_train / time_steps_train)
    
    time_steps = int(vocals.shape[1] / hop_size)
    n_samples = time_steps * hop_size

    
    gin_params = [
      'Additive.n_samples = {}'.format(n_samples),
      'FilteredNoise.n_samples = {}'.format(n_samples),
      'DefaultPreprocessor.time_steps = {}'.format(time_steps),
      'oscillator_bank.use_angular_cumsum = True',  # Avoids cumsum accumulation errors.
    ]
    #
    with gin.unlock_config():
      gin.parse_config(gin_params)
    #
    #
    #Trim all input vectors to correct lengths
    for key in ['f0_hz', 'f0_confidence', 'loudness_db']:
      vocals_features[key] = vocals_features[key][:time_steps]
      #vocals_features['audio'] = vocals_features['audio'][:, :n_samples]


    # Set up the model just to predict audio given new conditioning
    model = ddsp.training.models.Autoencoder()
    model.restore(ckpt)
    #
    # # Build model by running a batch through it.
    _ = model(vocals_features, training=False)
    #
    #
    # # %%
    #
    # Resynthesize Vocals
  
    vocals_features_mod = {k: v.copy() for k, v in vocals_features.items()}
    #
    #
    mask_on = None
    #
    #
    # ''' PRIMA BISOGNA RISOLVERE PICKLE
    if ADJUST and DATASET_STATS is not None:
      # Detect sections that are "on".
      mask_on, note_on_value = detect_notes(vocals_features['loudness_db'], vocals_features['f0_confidence'], vocals_threshold)
    #
      if np.any(mask_on):
        # Shift the pitch register.
        target_mean_pitch = DATASET_STATS['mean_pitch']
        pitch = ddsp.core.hz_to_midi(vocals_features['f0_hz'])
        mean_pitch = np.mean(pitch[mask_on])
        p_diff = target_mean_pitch - mean_pitch
        p_diff_octave = p_diff / 12.0
        round_fn = np.floor if p_diff_octave > 1.5 else np.ceil
        p_diff_octave = round_fn(p_diff_octave)
        vocals_features_mod = shift_f0(vocals_features_mod, p_diff_octave)
    #
    #
        # Quantile shift the note_on parts.
        _, loudness_norm = colab_utils.fit_quantile_transform(vocals_features['loudness_db'], mask_on, inv_quantile=DATASET_STATS['quantile_transform'])
    #
        # Turn down the note_off parts.
        mask_off = np.logical_not(mask_on)
        loudness_norm[mask_off] -=  vocals_quiet * (1.0 - note_on_value[mask_off][:, np.newaxis])
        loudness_norm = np.reshape(loudness_norm, vocals_features['loudness_db'].shape)
    #
        vocals_features_mod['loudness_db'] = loudness_norm
    #
    #
    #     # Auto-tune.
        #if autotune:
          #f0_midi = np.array(ddsp.core.hz_to_midi(vocals_features_mod['f0_hz']))
          #tuning_factor = get_tuning_factor(f0_midi, vocals_features_mod['f0_confidence'], mask_on)
          #f0_midi_at = auto_tune(f0_midi, tuning_factor, mask_on, amount=autotune)
          #vocals_features_mod['f0_hz'] = ddsp.core.midi_to_hz(f0_midi_at)
    #
    #
      else:
        print('\nSkipping auto-adjust (no notes detected or ADJUST box empty).')
    #
    else:
      print('\nSkipping auto-adujst (box not checked or no dataset statistics found).')
    #
    #
    # # Manual Shifts.
    vocals_features_mod = shift_ld(vocals_features_mod, vocals_loudness_shift)
    vocals_features_mod = shift_f0(vocals_features_mod, vocals_pitch_shift)
    #
    af = vocals_features if vocals_features_mod is None else vocals_features_mod
    #
    # # Run a batch of predictions.
    outputs = model(af, training=False)
    new_vocals = model.get_audio_from_outputs(outputs)

    # Write new_vocals into a file
    # If batched, take first element.
    if len(new_vocals.shape) == 2:
      new_vocals = new_vocals[0]

    normalizer = float(np.iinfo(np.int16).max)
    array_of_ints = np.array(
        np.asarray(new_vocals) * normalizer, dtype=np.int16)
    filename = "Generated_vocals.wav"
    wavfile.write(filename, DEFAULT_SAMPLE_RATE, array_of_ints)


  # BASS RESYNTHESIS
  
  if bass_present:    
    gin_file = os.path.join(bass_dir, 'operative_config-0.gin')
    
    
    # Load the dataset statistics.
    DATASET_STATS = None
    dataset_stats_file = os.path.join(bass_dir, 'dataset_statistics.pkl')
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
    ckpt_files = [f for f in tf.io.gfile.listdir(bass_dir) if 'ckpt' in f]
    ckpt_name = ckpt_files[0].split('.')[0]
    ckpt = os.path.join(bass_dir, ckpt_name)
    #
    # # Ensure dimensions and sampling rates are equal
    time_steps_train = gin.query_parameter('DefaultPreprocessor.time_steps')
    n_samples_train = gin.query_parameter('Additive.n_samples')
    hop_size = int(n_samples_train / time_steps_train)
    
    time_steps = int(vocals.shape[1] / hop_size)
    n_samples = time_steps * hop_size

    
    gin_params = [
      'Additive.n_samples = {}'.format(n_samples),
      'FilteredNoise.n_samples = {}'.format(n_samples),
      'DefaultPreprocessor.time_steps = {}'.format(time_steps),
      'oscillator_bank.use_angular_cumsum = True',  # Avoids cumsum accumulation errors.
    ]
    #
    with gin.unlock_config():
      gin.parse_config(gin_params)
    #
    #
    #Trim all input vectors to correct lengths
    for key in ['f0_hz', 'f0_confidence', 'loudness_db']:
      bass_features[key] = bass_features[key][:time_steps]
      #bass_features['audio'] = bass_features['audio'][:, :n_samples]


    # Set up the model just to predict audio given new conditioning
    model = ddsp.training.models.Autoencoder()
    model.restore(ckpt)
    #
    # # Build model by running a batch through it.
    _ = model(bass_features, training=False)
    #
    bass_features_mod = {k: v.copy() for k, v in bass_features.items()}
    #
    #
    mask_on = None
    #
    #
    # ''' PRIMA BISOGNA RISOLVERE PICKLE
    if ADJUST and DATASET_STATS is not None:
      # Detect sections that are "on".
      mask_on, note_on_value = detect_notes(bass_features['loudness_db'], bass_features['f0_confidence'], bass_threshold)
    #
      if np.any(mask_on):
        # Shift the pitch register.
        target_mean_pitch = DATASET_STATS['mean_pitch']
        pitch = ddsp.core.hz_to_midi(bass_features['f0_hz'])
        mean_pitch = np.mean(pitch[mask_on])
        p_diff = target_mean_pitch - mean_pitch
        p_diff_octave = p_diff / 12.0
        round_fn = np.floor if p_diff_octave > 1.5 else np.ceil
        p_diff_octave = round_fn(p_diff_octave)
        bass_features_mod = shift_f0(bass_features_mod, p_diff_octave)
    #
    #
        # Quantile shift the note_on parts.
        _, loudness_norm = colab_utils.fit_quantile_transform(bass_features['loudness_db'], mask_on, inv_quantile=DATASET_STATS['quantile_transform'])
    #
        # Turn down the note_off parts.
        mask_off = np.logical_not(mask_on)
        loudness_norm[mask_off] -=  bass_quiet * (1.0 - note_on_value[mask_off][:, np.newaxis])
        loudness_norm = np.reshape(loudness_norm, bass_features['loudness_db'].shape)
    #
        bass_features_mod['loudness_db'] = loudness_norm
    #
    #
    #     # Auto-tune.
        #if autotune:
          #f0_midi = np.array(ddsp.core.hz_to_midi(bass_features_mod['f0_hz']))
          #tuning_factor = get_tuning_factor(f0_midi, bass_features_mod['f0_confidence'], mask_on)
          #f0_midi_at = auto_tune(f0_midi, tuning_factor, mask_on, amount=autotune)
          #bass_features_mod['f0_hz'] = ddsp.core.midi_to_hz(f0_midi_at)
    #
    #
      else:
        print('\nSkipping auto-adjust (no notes detected or ADJUST box empty).')
    #
    else:
      print('\nSkipping auto-adujst (box not checked or no dataset statistics found).')
    #
    #
    # # Manual Shifts.
    bass_features_mod = shift_ld(bass_features_mod, bass_loudness_shift)
    bass_features_mod = shift_f0(bass_features_mod, bass_pitch_shift)
    #
    af = bass_features if bass_features_mod is None else bass_features_mod
    #
    # # Run a batch of predictions.
    outputs = model(af, training=False)
    new_bass = model.get_audio_from_outputs(outputs)

    # Write new_bass into a file
    # If batched, take first element.
    if len(new_bass.shape) == 2:
      new_bass = new_bass[0]

    normalizer = float(np.iinfo(np.int16).max)
    array_of_ints = np.array(
        np.asarray(new_bass) * normalizer, dtype=np.int16)
    filename = "Generated_bass.wav"
    wavfile.write(filename, DEFAULT_SAMPLE_RATE, array_of_ints)
  
  '''
  # Omnizart Transcribe and Resynthesize
  if drums_present:
  
    SF2_FILE = 'soundfonts/forest_soundfont.sf2'
    mode = "drum"
    
    print('Transcribing drums...')
    midi = dapp.transcribe(stem_drums, model_path=None)
    print('Drums transcribed!')

    print('Resynth drums...')
    # out_name = f"{uploaded_audio}_synth.wav"
    out_name = "New_drums.wav"
    #raw_wav = midi.fluidsynth(fs=44100, sf2_path=SF2_FILE)
    #wave.write(out_name, 44100, raw_wav)
    # soundscape_drum, sr = librosa.load(out_name, sr=16000)
    # print('Drums Resynthesized!')
    

  else:
    print('No drums found!')
  '''

  # Final Mix
  #
  mix = new_vocals + new_bass  #soundscape_drum[0:np.shape(audio_gen)[1]]
  if len(mix.shape) == 2:
      mix = mix[0]

  normalizer = float(np.iinfo(np.int16).max)
  array_of_ints = np.array(
      np.asarray(mix) * normalizer, dtype=np.int16)
  filename = "Soundscape.wav"
  wavfile.write(filename, DEFAULT_SAMPLE_RATE, array_of_ints)
  #
  

  # Per il background
  # if len(background) >= audio_gen.shape[-1]:
  #   background = background[0:audio_gen.shape[-1]]
