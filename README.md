<h1 align="center"> SOUNDSCAPE </h1>

<h3 align="center"> Hear differently </h3>

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
2. Choose the soundscape you'd like
3. Let the magic happen!

* The available soundscapes are _Mountain_, _Sea_ and _Pond_
* The song must contain at least some vocals or a bass line or a drum pattern or all of them to properly work.

<h3 align="center"> 
  <a href="https://www.youtube.com/watch?v=sBVO2PVux7Y&feature=emb_title" align="center"> WATCH A DEMO </a>
</h3>

## Mixer
<p align="center">
screenshot mixer
</p>

Once you have transformed the audio you can adjust the levels of all the tracks and eventually mute some of them.

## Implementation
The whole process is made of three main steps:

#### Source separation
The input audio is analysed and divided into four stems (Vocals, Bass, Drums, Accompaniment) using [Spleeter](https://github.com/deezer/spleeter) by Deezer

#### Timbre Transfer
Each available soundscape has two harmonic sounds which can be used to resynthesize the vocal and bass lines, if present, depending on their range. The timbre transfer and training of the models are performed by using [DDSPhttps://github.com/magenta/ddsp) by Magenta.

Each harmonic model is trained on a dataset containing between 15 and 20 minutes of the target sound. Due to the difficulty in finding those environmental sounds with a high variability, quality and length, data augmentation was performed making sure to keep the timbre equal through the whole dataset.

<p align="center">
  <img src="https://user-images.githubusercontent.com/57997005/109142121-cb842b80-775e-11eb-91d6-7fbe7cc13b2c.png" width="85%"//>
</p>

#### Drums Resynth
The drum track is resynthesized trying to match each drum sound with the most similar noise form the chose soundscape. This is done by using [Omnizart](https://github.com/Music-and-Culture-Technology-Lab/omnizart) by MCTLab.
For each soundscape a soundfont was created, containing a series of different sounds belonging to it with different envelopes in order to cover as many percussive sounds as possible.


## Hear some examples





## References 



## Notes
This application was developed as a project for the "Creative Programming and Computing" course at [Politecnico di Milano](https://www.polimi.it/en/) (MSc in Music and Acoustic Engineering).

*[Luigi Attorresi](https://github.com/LuigiAttorresi)*<br>
*[Federico Miotello](https://github.com/fmiotello)*
*[Giulio Zanetti](https://github.com/Hamalz)*<br>
