var elementSoundscape = document.getElementById('mySwipeSoundscape'),
    elementModality = document.getElementById('mySwipeModality'),
    prevBtnSoundscape = document.getElementById('prevSoundscape'),
    nextBtnSoundscape = document.getElementById('nextSoundscape'),
    prevBtnModality = document.getElementById('prevModality'),
    nextBtnModality = document.getElementById('nextModality'),
    mic = document.getElementById('microphone');

window.mySwipeSoundscape = new Swipe(elementSoundscape, {
  startSlide: 0,
  auto: 0,
  draggable: false,
  autoRestart: false,
  continuous: true,
  disableScroll: true,
  stopPropagation: true,
  callback: function(index, elementSoundscape) {},
  transitionEnd: function(index, elementSoundscape) {}
});

window.mySwipeModality = new Swipe(elementModality, {
  startSlide: 0,
  auto: 0,
  draggable: false,
  autoRestart: false,
  continuous: true,
  disableScroll: true,
  stopPropagation: true,
  callback: function(index, elementModality) {},
  transitionEnd: function(index, elementModality) {}
});

var audio_sea = new Audio('../static/audio/sea.mp3');
var audio_mountain = new Audio('../static/audio/mountain.mp3');
var audio_pond = new Audio('../static/audio/pond.mp3');
audio_sea.loop = "true";
audio_mountain.loop = "true";
audio_pond.loop = "true";

let update_bg = function () {
  var soundscape = document.getElementById("soundscape_selection").value
  var background = document.getElementById('dynamic-background');
  if (soundscape == 'sea') {
    background.style.backgroundImage = 'url(../static/images/sea.jpg)';
    if (!muted) {
      audio_sea.play();
      audio_mountain.pause();
      audio_pond.pause();
    }
  }
  else if (soundscape == 'mountain') {
    background.style.backgroundImage = 'url(../static/images/mountain.jpg)';
    if (!muted) {
      audio_sea.pause();
      audio_mountain.play();
      audio_pond.pause();
    }
  }
  else if (soundscape == 'pond') {
    background.style.backgroundImage = 'url(../static/images/pond.jpg)';
    if (!muted) {
      audio_sea.pause();
      audio_mountain.pause();
      audio_pond.play();
    }
  }
}

let indexSoundscape = 0;
let indexModality = 0;
let modalities = ['sample', 'upload', 'record'];

let mod = function (x, m) {
    return (x%m + m)%m;
}

let prevSelectedSoundscape = function () {
    mySwipeSoundscape.prev();
    document.getElementById("soundscape_selection").value = scapes[mod(--indexSoundscape, scapes.length)];
    console.log(document.getElementById("soundscape_selection").value)
    update_bg()

}

let nextSelectedSoundscape = function () {
    mySwipeSoundscape.next();
    document.getElementById("soundscape_selection").value = scapes[mod(++indexSoundscape, scapes.length)];
    console.log(document.getElementById("soundscape_selection").value)
    update_bg()
}

let prevSelectedModality = function () {
    mySwipeModality.prev();
    document.getElementById("modality_selection").value = modalities[mod(--indexModality, scapes.length)];
    console.log(document.getElementById("modality_selection").value)
}

let nextSelectedModality = function () {
    mySwipeModality.next();
    document.getElementById("modality_selection").value = modalities[mod(++indexModality, scapes.length)];
    console.log(document.getElementById("modality_selection").value)
}

prevBtnSoundscape.onclick = prevSelectedSoundscape;
nextBtnSoundscape.onclick = nextSelectedSoundscape;

prevBtnModality.onclick = prevSelectedModality;
nextBtnModality.onclick = nextSelectedModality;

console.log(document.getElementById("soundscape_selection").value);
console.log(document.getElementById("modality_selection").value);
//update_bg()
document.getElementById('dynamic-background').style.backgroundImage = 'url(../static/images/mountain.jpg)';


var uploadDefault = false;
var uploadRecord = false;
var uploadSong = false;

//Microphone

'use strict'

let log = console.log.bind(console),
    id = val => document.getElementById(val),
    ul = id('ul'),
    gUMbtn = id('gUMbtn'),
    start = id('start'),
    stop = id('stop'),
    stream,
    recorder,
    counter=1,
    chunks,
    media;

id('btns').style.display = 'none';

gUMbtn.onclick = e => {
    let mediaOptions = {
            audio: {
            tag: 'audio',
            type: 'audio/wav',
            ext: '.wav',
            gUM: {audio: true}
        }
    };
    media = mediaOptions.audio;
    navigator.mediaDevices.getUserMedia(media.gUM).then(_stream => {
        stream = _stream;
        id('gUMArea').style.display = 'none';
        id('btns').style.display = 'inherit';
        start.removeAttribute('disabled');
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = e => {
        chunks.push(e.data);
        if(recorder.state == 'inactive') {
          makeLink();
          console.log('Link Made')
        }
        };
        log('got media successfully');
    }).catch(log);
}

start.onclick = e => {
    start.disabled = true;
    stop.removeAttribute('disabled');
    chunks=[];
    recorder.start();
}

stop.onclick = e => {
    stop.disabled = true;
    recorder.stop();
    start.removeAttribute('disabled');
    id('btns').style.display = 'none';
}

function makeLink(){
    let blob = new File(chunks, "recording.wav", {type: media.type })
        , url = URL.createObjectURL(blob)
        , li = document.createElement('li')
        , mt = document.createElement(media.tag)
        , hf = document.createElement('a');
    console.log(blob.name)
    mt.controls = true;
    mt.src = url;
    mt.id = 'audio-player'
    hf.href = url;
    li.appendChild(mt);
    li.appendChild(hf);
    ul.appendChild(li);

    let list = new DataTransfer();
    list.items.add(blob);
    let myFileList = list.files;
    id('song-recorder').files = myFileList;
    console.log(id('song-recorder').files[0]);

    let recorded_file = id("song-recorder").files[0];
    let formDataRec = new FormData();
    formDataRec.append("recorded_file", recorded_file);
    fetch('/audio', {method: "POST", body: formDataRec});
}

// mic.addEventListener("click", function() {
//   mic.classList.toggle("active")
//   if(mic.classList.contains("active")) {
//
//   } else {
//
//   }
// });

//Upload button animation
var button, parent;

button = document.getElementById('update-button');

parent = button.parentElement;

// button.addEventListener("click", function() {
//   parent.classList.add("clicked");
//   return setTimeout((function() {
//     uploadSong = true;
//     return parent.classList.add("success");
//   }), 2600);
// });


let uploaded_song = document.getElementById("song-uploader").files[0];
let formDataUp = new FormData();

formDataUp.append("uploaded_song", uploaded_song);
fetch('/audio', {method: "POST", body: formDataUp});


var start_button = document.getElementById("start_button");

start_button.addEventListener("click", function() {
  index_form.submit()
});

var muted = true;

let muteUnmute = function() {
  muted = !muted;
  var icon = document.getElementById("mute-icon");
  icon.classList.toggle("fa-volume-mute");
  icon.classList.toggle("fa-volume-up");
  update_bg()
  if (muted) {
    audio_sea.pause();
    audio_mountain.pause();
    audio_pond.pause();
  }
}

window.muteUnmute = muteUnmute;

function fileUploaded() {
    let file = document.getElementById("song-uploader");
    document.getElementById("file-not-uploaded").style.display = 'none';
    document.getElementById("file-uploaded").style.display = 'inherit';
}

window.fileUploaded = fileUploaded;
