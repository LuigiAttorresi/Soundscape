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

let update_bg = function () {
  var soundscape = document.getElementById("soundscape_selection").value
  var background = document.getElementById('dynamic-background');
  if (soundscape == 'sea') {
    background.style.backgroundImage = 'url(../static/images/sea.jpg)';
  }
  if (soundscape == 'mountain') {
    background.style.backgroundImage = 'url(../static/images/mountain.jpg)';
  }
  if (soundscape == 'pond') {
    background.style.backgroundImage = 'url(../static/images/pond.jpg)';
  }
}

let indexSoundscape = 0;
let indexModality = 0;
let modalities = ['sample', 'record', 'upload'];

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
    document.getElementById("modality_selection").value = modalities[mod(++indexModality, scapes.length)];
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
update_bg()





var uploadDefault = false;
var uploadRecord = false;
var uploadSong = false;

//Microphone
mic.addEventListener("click", function() {
  mic.classList.toggle("active")
  discardDefault()
  discardSong()
  uploadRecord = true;
});

//Upload button animation
var button, parent;

button = document.getElementById('update-button');

parent = button.parentElement;

button.addEventListener("click", function() {
  parent.classList.add("clicked");
  return setTimeout((function() {
    discardRecording();
    discardDefault();
    uploadSong = true;
    return parent.classList.add("success");
  }), 2600);
});


let discardRecording = function () {
  uploadRecord = false;
  if (mic.classList.contains("active")) {
    mic.classList.remove("active")
    // TODO stop recording
  }
  // TODO delete recording
}

let discardDefault = function () {
  uploadDefault = false;
  // TODO delete uploaded song
}

let discardSong = function () {
  uploadSong = false;
  if (parent.classList.contains("clicked")) {
    parent.classList.remove("clicked")
  }
  if (parent.classList.contains("success")) {
    parent.classList.remove("success")  
  }
  // TODO delete upload
}

let uploaded_song = document.getElementById("song-uploader").files[0];
let formData = new FormData();
     
formData.append("uploaded_song", uploaded_song);
fetch('/audio', {method: "POST", body: formData});