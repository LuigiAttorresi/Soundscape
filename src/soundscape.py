# http://127.0.0.1:5000/


###########
# IMPORTS #
###########


import record
import resynthesis
import separation
import params
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template, request, url_for, session, redirect
import os


######################
#  GLABAL VARIABLES  #
# AND INITIALIZATION #
######################


params.init_params()
vocal_parameters = None
bass_parameters = None


#############
# FUNCTIONS #
#############

def change_soundscape(soundscape):
    vocal_parameters = soundscape_params[soundscape]['vocal_params']
    bass_parameters = soundscape_params[soundscape]['bass_params']


TEMPLATE_DIR = os.path.abspath('src/templates')
STATIC_DIR = os.path.abspath('src/static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
       session['selected_song'] = request.form.get('sample_song_selection')
       session['selected_soundscape'] = request.form.get('soundscape_selection')
       change_soundscape(session['selected_soundscape'])
       return redirect(url_for('resynth'))

    audio_dir = 'audio'
    audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]
    return render_template('index.html', sample_songs=audio_files, soundscapes=soundscapes)

@app.route('/resynth', methods=['GET', 'POST'])
def resynth():
    return render_template('resynth.html', selected_song = session['selected_song'], selected_soundscape = session['selected_soundscape'])


########
# MAIN #
########


if __name__ == "__main__":

  app.run(debug=True)

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
