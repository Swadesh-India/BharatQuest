import AnimationEngine from '/static/src/animax.js';
const box = document.getElementsByClassName('categ-box-opt')
Array.from(box).forEach((b) => {
  b.addEventListener('click',(e) =>{
   const query = e.target.innerText
   location.href = 'search/results?query='+query;
  } )
})

const tabs = document.getElementsByClassName('tabs')
Array.from(tabs).forEach((tab) =>{
  tab.addEventListener('click',(e) =>{
  
    e.stopPropagation()
    const text = e.currentTarget.dataset.value;
    location.href = 'search/results?query='+text;

  } )
} )
const categ = document.getElementsByClassName('category-box')
Array.from(categ).forEach((cat) => {
  cat.addEventListener('click', (e) => {
    e.stopPropagation()
    const text = e.currentTarget.children[1].innerText
    location.href = 'search/results?query=' + text;
    
  })
})



//animation work 

const getStartBtn = document.querySelector('.get-started');
function addText(el,text,time,delay) {
  const chars = text.split('');
  
  const timePerChar = time/chars.length;
  let i=0
  el.text=""
  let interval;
  setTimeout(() =>{
    
    interval=setInterval(displayText,timePerChar*1000)
  }, delay*1000)
  function displayText() {
  el.textContent += chars[i]
  
  i++;
if(i>=chars.length) clearInterval(interval);
  }
}
if(getStartBtn){
  
addText(getStartBtn.children[0],getStartBtn.children[0].innerText,0.6,1.4)


}
const infotab = document.querySelector('.infotabs')



const Engine1 = new AnimationEngine(infotab);
Engine1.visibilityObserver(slideTop,slideDown,{threshold:0.2})
function slideTop(el,observer) {
el.classList.add('moveBoxUp');
el.classList.remove('moveBoxDown')
observer.unobserve(el)
}
function slideDown(el,observer) {
el.classList.add('moveBoxDown')

}

const Engine2 = new AnimationEngine(categ);
Engine2.visibilityObserver(function(el,observer){
  el.classList.add('visible')
  observer.unobserve(el)
},function(el){
  try {el.classList.remove('visible')}
  catch(e){}
},{threshold:0.1})


const categDesc = document.querySelector('.categ-desc')
const Engine3 = new AnimationEngine(categDesc)

Engine3.visibilityObserver(function(el){
  el.classList.add('categ-desc-visible')
  
},function(el){
  try {el.classList.remove('categ-desc-visible')}
  catch(e){}
},{threshold:0.1})

const about = document.querySelector('.about')
const Engine4 = new AnimationEngine(about)

Engine4.visibilityObserver(function(el){
  el.classList.add('about-visible')
},function(el){
  try {el.classList.remove('about-visible')
  }
  catch(e){}
},{threshold:0.1})


