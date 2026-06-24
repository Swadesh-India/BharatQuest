export default class AnimationEngine{
  constructor(el,duration, delay) {
    if (!el && el.nodeType!='1' && el.constructor.name!=='NodeList') {
      throw new Error(`AnimationEngine : ${el} mist be a HTML element or nodeList`)
    }
      this.el=el
      this.duration=duration
      this.delay=delay
    
  }
  visibilityObserver(trueFunc,falseFunc,{threshold,rootMargin}){
  if (!trueFunc || !falseFunc) {
    throw new Error('AnimationEngine : Handler functions are not given')
  }
    const observer= new IntersectionObserver(function(entries){
      entries.forEach((entry) =>{
        if (entry.isIntersecting) {
          trueFunc(entry.target,observer)
        }else{falseFunc(entry.target)}
      } )
    },{threshold, rootMargin})
    if (this.el.constructor.name==='HTMLCollection') {
      Array.from(this.el).forEach((elem) =>observer.observe(elem) )
    } else {
      observer.observe(this.el,observer)
    }
  }
}