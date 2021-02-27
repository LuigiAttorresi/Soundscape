# http://127.0.0.1:5000/


###########
# IMPORTS #
###########

import os
import record
import resynthesis
import separation
import params
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
from flask import Flask, render_template, request, url_for, session, redirect, send_from_directory


######################
#  GLABAL VARIABLES  #
# AND INITIALIZATION #
######################


params.init_params()


#############
# FUNCTIONS #
#############

def change_soundscape(soundscape):
    params.vocal_parameters = params.soundscape_params[soundscape]['vocal_params']
    params.bass_parameters = params.soundscape_params[soundscape]['bass_params']
    params.soundfont = params.soundscape_params[soundscape]['soundfont']
    params.background = params.soundscape_params[soundscape]['background']


TEMPLATE_DIR = os.path.abspath('src/templates')
STATIC_DIR = os.path.abspath('src/static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_folder = os.path.join('audio')
    output_folder = os.path.join('output')
    soundfont_folder = os.path.join('soundfonts')
    bg_folder = os.path.join('backgrounds')

    if request.method == 'POST':
        session['selected_song'] = request.form.get('sample_song_selection')
        session['selected_soundscape'] = request.form.get('soundscape_selection')

        change_soundscape(session['selected_soundscape'])

        audio_file_name = session['selected_song']
        soundfont_path = os.path.join(soundfont_folder, params.soundfont)
        bg_path = os.path.join(bg_folder, params.background)

        print('Starting separation...')
        separation.separate(audio_file_name)
        print('Separation done!')
        vocals, _= separation.get_stem_array(audio_file_name,'vocals')
        bass, _= separation.get_stem_array(audio_file_name,'bass')
        drums, _= separation.get_stem_array(audio_file_name,'drums')
        other, _= separation.get_stem_array(audio_file_name,'other')

        drum_path = os.path.join(output_folder, audio_file_name.split('.')[0], 'drums.wav')
        vocals_present = separation.is_present(vocals)
        bass_present = separation.is_present(bass)
        drums_present = separation.is_present(drums)

        print('Starting resynth...')

        if vocals_present:
            new_vocals = resynthesis.resynth(vocals, params.vocal_parameters)
            audio_length = len(new_vocals)

        if bass_present:
            new_bass = resynthesis.resynth(bass, params.bass_parameters)
            audio_length = len(new_bass)

        if drums_present:                                                             #Scommentare da Mac
            new_drums = resynthesis.drum_resynth(drum_path, soundfont_path)           #Scommentare da Mac

        if vocals_present or bass_present or drums_present:
            background = resynthesis.generate_background(bg_path, audio_length)
            other = resynthesis.adjust_length(other, audio_length)
            new_drums = resynthesis.adjust_length(new_drums, audio_length)            #Scommentare da Mac
        else:
            print("The input song must contain at least vocals or bass or drums!")
            # return redirect(url_for(error_page))

        print('Resynth done!')

        # FINAL MIX
        mix = 0.5*new_vocals + 1.5*new_bass + 0.5*other + 0.5*background + new_drums    #Scommentare da Mac

        if len(mix.shape) == 2:
            mix = mix[0]

        normalizer = float(np.iinfo(np.int16).max)
        array_of_ints = np.array(np.asarray(mix) * normalizer, dtype=np.int16)
        filename = "soundscape.wav"
        wavfile.write(filename, 16000, array_of_ints)

        if len(other.shape) == 2:
            other = other[0]

        normalizer = float(np.iinfo(np.int16).max)
        array_of_ints = np.array(np.asarray(other) * normalizer, dtype=np.int16)
        filename = "other.wav"
        wavfile.write(filename, 16000, array_of_ints)

        if len(background.shape) == 2:
            background = background[0]

        normalizer = float(np.iinfo(np.int16).max)
        array_of_ints = np.array(np.asarray(background) * normalizer, dtype=np.int16)
        filename = "background.wav"
        wavfile.write(filename, 16000, array_of_ints)

        return redirect(url_for('resynth'))

    audio_files = [f for f in os.listdir(audio_folder) if os.path.isfile(os.path.join(audio_folder, f))]
    return render_template('index.html', sample_songs=audio_files, soundscapes=params.soundscapes)


@app.route('/resynth', methods=['GET', 'POST'])
def resynth():
    return render_template('resynth.html', selected_song = session['selected_song'], selected_soundscape = session['selected_soundscape'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


########
# MAIN #
########

if __name__ == "__main__":

    app.run(debug=True)
