# Soundscape
## Installation instructions:
```bash
# Create python virtual environment and activate it:
py -m venv soundscape-venv
.\soundscape-venv\Scripts\activate

# Install dependencies and download required data:
pip install -U pip
pip install cython
pip install numpy
pip install -r requirements.txt
omnizart download-checkpoints
```

Substitute  ``soundscape-venv\Lib\site-packages\omnizart\drum\labels.py`` and ``soundscape-venv\Lib\site-packages\ddsp\colab\colab_utils.py`` with the provided ``labels.py`` and ``colab_utils.py`` files.