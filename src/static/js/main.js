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
