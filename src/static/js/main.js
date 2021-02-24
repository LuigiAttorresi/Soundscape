var element = document.getElementById('mySwipe');
window.mySwipe = new Swipe(element, {
  startSlide: 0,
  auto: 3000,
  draggable: false,
  autoRestart: false,
  continuous: true,
  disableScroll: true,
  stopPropagation: true,
  callback: function(index, element) {},
  transitionEnd: function(index, element) {}
});