print('Start feature input')

import crepe
import ddsp
import ddsp.training
import separation
import numpy as np

print('End feature input')

#Just for testing
import time

# Setup the session.
ddsp.spectral_ops.reset_crepe()

# Compute features.
def extract_features(audio_array):
    if separation.is_present(audio_array):
        audio_array = audio_array[np.newaxis, :]
        start_time = time.time()
        features = ddsp.training.metrics.compute_audio_features(audio_array)
        features['loudness_db'] = features['loudness_db'].astype(np.float32)
        print('Audio features took %.1f seconds' % (time.time() - start_time))
        features_mod = None   
        return features, features_mod

# TRIM = -15