var elementSoundscape = document.getElementById('mySwipeSoundscape'),
    elementModality = document.getElementById('mySwipeModality'),
    prevBtnSoundscape = document.getElementById('prevSoundscape'),
    nextBtnSoundscape = document.getElementById('nextSoundscape'),
    prevBtnModality = document.getElementById('prevModality'),
    nextBtnModality = document.getElementById('nextModality');

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

let index = 0;

let mod = function (x, m) {
    return (x%m + m)%m;
}

let prevSelectedSoundscape = function () {
    mySwipeSoundscape.prev();
    document.getElementById("soundscape_selection").value = scapes[mod(--index, scapes.length)];
    console.log(document.getElementById("soundscape_selection").value)
}

let nextSelectedSoundscape = function () {
    mySwipeSoundscape.next();
    document.getElementById("soundscape_selection").value = scapes[mod(++index, scapes.length)];
    console.log(document.getElementById("soundscape_selection").value)
}


prevBtnSoundscape.onclick = prevSelectedSoundscape;
nextBtnSoundscape.onclick = nextSelectedSoundscape;

prevBtnModality.onclick = mySwipeModality.prev;
nextBtnModality.onclick = mySwipeModality.next;

/*
var upload_swipe = document.getElementById('uploadSwipe'),
    soundscape_swipe = document.getElementById('sdounscapeSwipe'),
    prevBtnUpload = document.getElementById('rightArrowUpload'),
    nextBtnUpload = document.getElementById('leftArrowUpload'),
    prevBtnSoundscape = document.getElementById('rightArrowSoundscape'),
    nextBtnSoundscape = document.getElementById('rightArrowSoundscape'),
    mic = document.getElementById('microphone');


soundscape_swipe = new Swipe(soundscape_swipe, {
  startSlide: 0,
  auto: 0,
  draggable: false,
  autoRestart: false,
  continuous: true,
  disableScroll: true,
  stopPropagation: true,
  callback: function(index, soundscape_swipe) {},
  transitionEnd: function(index, soundscape_swipe) {}
});

upload_swipe = new Swipe(upload_swipe, {
  startSlide: 0,
  auto: 0,
  draggable: false,
  autoRestart: false,
  continuous: true,
  disableScroll: true,
  stopPropagation: true,
  callback: function(index, upload_swipe) {},
  transitionEnd: function(index, upload_swipe) {}
});



prevBtnUpload.onclick = upload_swipe.prev;
nextBtnUpload.onclick = upload_swipe.next;

prevBtnSoundscape.onclick = soundscape_swipe.prev;
nextBtnSoundscape.onclick = soundscape_swipe.next;
mic.onclick = mic.classList.toggle('active')
//mic.onclick = console.log("click")

*/
