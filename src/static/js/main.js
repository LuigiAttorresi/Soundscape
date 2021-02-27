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

console.log(document.getElementById("soundscape_selection").value)
update_bg()
