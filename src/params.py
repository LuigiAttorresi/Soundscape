soundscapes = ['mountain', 'pond', 'sea']

### GLOBAL PARAMS OF A SOUNDSCAPE

vocal_parameters = None
bass_parameters = None
soundfont = None
background = None

### POND

pond_vocal_parameters = {
  'type': 'vocals',
  'dir': 'models/Anatra40K',
  'threshold': 1,
  'quiet': 20,
  'autotune': 0,
  'loudness_shift': 0,
  'pitch_shift': 0
}

pond_bass_parameters = {
  'type': 'bass',
  'dir': 'models/Mosca12K',
  'threshold': 1,
  'quiet': 20,
  'autotune': 0,
  'loudness_shift': 0,
  'pitch_shift': 0
}

# MOUNTAIN

mountain_vocal_parameters = {
  'type': 'vocals',
  'dir': 'models/Motosega10K',
  'threshold': 1,
  'quiet': 20,
  'autotune': 0,
  'loudness_shift': 0,
  'pitch_shift': 0
}

mountain_bass_parameters = {
  'type': 'bass',
  'dir': 'models/Mucca40K',
  'threshold': 1,
  'quiet': 20,
  'autotune': 0,
  'loudness_shift': 0,
  'pitch_shift': -1
}

### SEA

sea_vocal_parameters = {
  'type': 'vocals',
  'dir': 'models/Gabbiano40K',
  'threshold': 1,
  'quiet': 20,
  'autotune': 0,
  'loudness_shift': 0,
  'pitch_shift': 0
}

sea_bass_parameters = {
  'type': 'bass',
  'dir': 'models/Barca40K',
  'threshold': 1,
  'quiet': 20,
  'autotune': 0,
  'loudness_shift': 0,
  'pitch_shift': -1
}

soundscape_params = {}

def init_params():
    for soundscape in soundscapes:
        soundscape_params[soundscape] = {
            'vocal_params': eval(soundscape + '_vocal_parameters'),
            'bass_params': eval(soundscape + '_bass_parameters'),
            'soundfont': soundscape + '_soundfont.sf2',
            'background': soundscape + '_bg.wav'
        }
