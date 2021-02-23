import crepe
import ddsp
import ddsp.training
import separation
import numpy as np


# Setup the session.
ddsp.spectral_ops.reset_crepe()

# Compute features.
def extract_features(audio_array):
    if separation.is_present(audio_array):
        features = ddsp.training.metrics.compute_audio_features(audio_array)
        features['loudness_db'] = features['loudness_db'].astype(np.float32)
        features_mod = None   
        return features, features_mod

# TRIM = -15