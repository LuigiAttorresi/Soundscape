<p align="center">
  <img src="https://user-images.githubusercontent.com/57997005/109641068-90646c80-7b51-11eb-85b8-1ef923a57741.png"//>
</p>

<p align="center">
  Screenshot interfaccia
</p>

<h2 align="center">
<a href="https://gabristucchi.github.io/Spicer/" align="center"> TRY IT </a>
</h2>

## How To Use
The environments we daily deal with constantly provide us with sounds, melodies and noises generating different soundscapes, but have you ever wondered how a song you like would sound in those context?
Here is the the goal of _Soundscape_, a Web application meant to make you feel the sounds that surround you in a different way, creating a special bond between music and nature.

<p align="center">
  <img src="https://user-images.githubusercontent.com/57997005/109137421-798cd700-7759-11eb-909e-8372019e7e82.png" width="85%"//>
</p>


1. Select, upload or record a song
2. Choose the soundscape you like
3. Hear the result!

* The available soundscapes are _Srping Mountain_, _Sea Life_ and _Natural Pond_
* The song must contain at least some vocals or a bass line or a drum pattern or all of them to properly work.

<h3 align="center"> 
  <a href="https://www.youtube.com/watch?v=sBVO2PVux7Y&feature=emb_title" align="center"> WATCH A DEMO </a>
</h3>

## Implementation
The whole process is made of three main steps:

#### Source Separation
The input audio is analysed and divided into four stems (Vocals, Bass, Drums, Accompaniment) using [Spleeter](https://github.com/deezer/spleeter) by Deezer, all extracted at 16kHz.
Then for each stem the RMS energy is computed to check if it actually the track is present.

#### Harmonic Components
Each available soundscape has two harmonic sounds which can be used to resynthesize the vocal and bass lines, if present, depending on their range. This is done by performing timbre transfer thanks to [DDSP](https://github.com/magenta/ddsp) by Magenta.

<p align="center">
  <img src="https://user-images.githubusercontent.com/57997005/109142121-cb842b80-775e-11eb-91d6-7fbe7cc13b2c.png" width="85%"//>
</p>

Each harmonic model is trained on a dataset containing between 15 and 20 minutes of the target sound. Due to the difficulty in finding those environmental sounds with a high variability, quality and length, data augmentation was performed making sure to keep the timbre equal through the whole dataset. A preprocessing step of denoising and compressioin was also necessary.

#### Percussive Components
The percussive part is resynthesized trying to match each drum sound with the most similar noise form the chose soundscape. This is done by using [Omnizart](https://github.com/Music-and-Culture-Technology-Lab/omnizart) by MCTLab.
The percussive sound analyisis and classification regards four types of sounds: Hi-hat, Kick, Snare and Clap. A randomization of similar soundfont sounds is performed to obtain variety.
For each soundscape a soundfont was created, containing a series of different sounds belonging to it with different envelopes in order to cover as many percussive sounds as possible.

## Hear some examples



## Notes
This application was developed as a project for the "Creative Programming and Computing" course at [Politecnico di Milano](https://www.polimi.it/en/) (MSc in Music and Acoustic Engineering).

*[Luigi Attorresi](https://github.com/LuigiAttorresi)*<br>
*[Federico Miotello](https://github.com/fmiotello)*<br>
*[Giulio Zanetti](https://github.com/Hamalz)*<br>
