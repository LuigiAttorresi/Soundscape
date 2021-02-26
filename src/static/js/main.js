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


