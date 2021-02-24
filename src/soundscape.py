# http://127.0.0.1:5000/

import record 
import resynthesis
import separation
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template, request, url_for
import os

vocal_parameters = {
  "type": 'vocals',
  "dir": 'models/Anatra40K',
  "threshold": 1,
  "quiet": 20,
  "autotune": 0,
  "loudness_shift": 0,
  "pitch_shift": 0
}

bass_parameters = {
  "type": 'bass',
  "dir": 'models/Mosca12K',
  "threshold": 1,
  "quiet": 20,
  "autotune": 0,
  "loudness_shift": 0,
  "pitch_shift": 0
}

TEMPLATE_DIR = os.path.abspath('src/templates')
STATIC_DIR = os.path.abspath('src/static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
       option = request.form.get('options')
       print(option)
       print(url_for('static', filename='css/main.css'))
    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)


 

 
  '''
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
    # DRUMS 
    # drums_dir

    # BACKGROUND
    background_dir = 'audio\celeste.wav'
        
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
  '''



  '''
  # BACKGROUND DA FINIRE
  background, sr = librosa.load(background_dir, sr=16000)
  if len(background) >= audio.shape[-1]:
    background = background[0:vocals.shape[-1]]


  
  # FINAL MIX
  mix = new_vocals + new_bass + 0.5 * other + 0.5*background #+ soundscape_drum[0:np.shape(audio_gen)[1]]
  if len(mix.shape) == 2:
      mix = mix[0]

  normalizer = float(np.iinfo(np.int16).max)
  array_of_ints = np.array(
      np.asarray(mix) * normalizer, dtype=np.int16)
  filename = "soundscape.wav"
  wavfile.write(filename, DEFAULT_SAMPLE_RATE, array_of_ints)
  '''
 