const slideAuthImg=document.querySelectorAll('.slide-auth-img')
/*Array.from(slideAuthImg).forEach((img) =>{
  img.style.width= getComputedStyle(img).height
} )*/
const slideImages = document.querySelectorAll(".article-img-cont img")
const articleImages = document.querySelectorAll(".slide-image img")

slideImages.forEach(handleSize)
articleImages.forEach(handleSize)

function applySize(img) {
let aspectRatio=img.naturalWidth/img.naturalHeight
  if(aspectRatio>1){
    img.style.height='100%'
  }else{
    img.style.width='100%'

  }
}
function handleSize(img) {
  
  if (img.complete) {
    applySize(img)
  } else {
    img.onload=()=>{applySize(img)}
  }
}


const slides = document.querySelectorAll('.slide, .article-card');  

Array.from(slides).forEach((slide) => {
  slide.addEventListener('click',(e)=>{
    console.log("clicked");
    
    const link = slide.querySelector('a')
    location.href=link.href
  })
})

function relativeTime(date) {
  const now = new Date()
  const then = new Date(date)
  const timePassed = (now -then)/1000/3600;

  if (timePassed<1/60) {
    return 'just now'
  }
  else if (timePassed<1) {
    return `${Math.floor(timePassed*60)} min ago`
  }
  else if (timePassed<=24) {
    return `${Math.floor(timePassed)} hours ago`
  }else if(timePassed<=48){
    return 'yesterday'
  }else if (timePassed<24*7) {
    return `${Math.floor(timePassed/24)} days ago`
  }else if (timePassed<=24*30){
  return `${Math.floor(timePassed/24/7)} ${Math.floor(timePassed/24/7)==1 ?'week':'weeks'} ago`
  }else if (timePassed <=365*24){
    return `${Math.floor(timePassed/24/30)} ${Math.floor(timePassed/24/30)==1 ?'month':'months'} ago`
  }else if(timePassed>365*24){
    return `${Math.floor(timePassed/24/365)} ${Math.floor(timePassed/24/365)==1 ?'year':'years'} ago`
  }
}

const timeStamp = document.querySelectorAll('.slide-time-stamp')
Array.from((timeStamp)).forEach((st) =>{
  st.innerText= relativeTime(st.dataset.date)
} )



const addBlogBtn = document.getElementById('add-blog-wrapper');
addBlogBtn.addEventListener('click', (e) => {
  console.log("clicked");
  
  location.href=addBlogBtn.dataset.redirecturl
});