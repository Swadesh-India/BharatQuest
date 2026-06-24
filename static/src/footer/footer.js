import AnimationEngine from '../animax.js';

const footer = document.querySelector('footer')
const Engine4 = new AnimationEngine(footer)

Engine4.visibilityObserver(function(el) {
  el.classList.add('footer-visible')
}, function(el) {
  try {
    el.classList.remove('footer-visible')
  }
  catch (e) {}
}, { threshold: 0.1 })
