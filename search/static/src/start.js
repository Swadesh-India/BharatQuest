import {generateData} from './dataretrivalsystem.js';
const params = new URLSearchParams(window.location.search);
const query = params.get('query');
const factContainer = document.getElementById('quick-facts')
const titleCont= document.querySelector('.title')
const generalMessage = `Note: if my title is somthing that nit have any meaning or it is not a festival, culture, or dishes, or monuments, then just reply 'enter correct keyword'
Note: strictly note that if my title is not a direct name of monument, culture, festival or dish.then just reply again 'Enter correct keyword'`
async function generateFacts(query){
  let prompt = `Tell me about ${query}. Strictly: only give the required answer. dont write any extra text or message. you have yo tell some fact a about ${query}. Answer format: 		
  <ul id="quick-facts-list">
			<li id="fact-date"><strong>Date:</strong> <span id="date-detail">Time</span></li>
			<li id="fact-significance"><strong>Significance:</strong> <span id="significance-detail">significance</span></li>
			<li id="fact-states"><strong>States:</strong> <span id="states-detail">location</span></li>
		</ul>
		
		etc
		You can add more facts. but give the answer strictly in this forma
		
		${generalMessage}`
		
  
  const res= await generateData(prompt);
  
  const result =  (res).replace(/```html/g, '').replace(/`/g,'')
  
  return result;
}
async function generateTitle(query) {
	const prompt=`I am writing an article on ${query}. generate a one linear title for my article. Struct Note: do not give any other message in your response and tell the title directly,
		${generalMessage}`
return  (await generateData(prompt));

	
}

async function generateOrigin() {
	const originPrompt = `I am writing an article on ${query}. I want to write about its origin. so tell me about origin of ${query}.Start with metioning a title 'origin'.Surround it in h3 tag. you can use few emojis. Strictly Note: do not give any other message in your response tell the origin directly,
	${generalMessage}`

	return  (await generateData(originPrompt)).replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>').replace(/\*/g, '&bull;');
}
async function generateTip() {
	const tipPrompt = `I am writing an article on ${query}. I want to include some tips about it. so tell me some tips for ${query}. Start with metioning a title 'tip'. Surround it in h3 tag.you can use few emojis. Strictly Note: do not give any other message in your response tell the tips directly,
	${generalMessage}`

	return  (await generateData(tipPrompt)).replace(/\*\*(.*?)\*\*/g,'<b>$1</b>').replace(/\n/g,'<br>').replace(/\*/g,'&bull;');

	
}
async function generateTradition() {
	const traditionPrompt = `I am writing an article on ${query}. I want to include some traditions celebrated in it.Start with metioning a title 'Tradition'.Surround it in h3 tag. you can use few emojis.  so tell me about some traditions for ${query}. Strictly Note: do not give any other message in your response tell the traditions directly,
	${generalMessage}`
return  (await generateData(traditionPrompt)).replace(/\*\*(.*?)\*\*/g,'<b>$1</b>').replace(/\n/g,'<br>').replace(/\*/g,'&bull;');

	
}
async function generateFood() {
	const foodPrompt = `I am writing an article on ${query}. I want to include some foods about it. so tell me some food for ${query}.Start with metioning a title 'Food'. Surround it in h3 html tag.you can use few emojis. Give hour answer in unordered list form. dont mention whole html. write only list part  Strictly Note: do not give any other message in your response tell the foods directly,
	${generalMessage}
	`
	
	
return  (await generateData(foodPrompt)).replace(/\*\*(.*?)\*\*/g,'<b>$1</b>').replace(/\n/g,'<br>').replace(/\*/g,'&bull;');


	
}
async function display(query) {
generateFacts(query).then((res) =>render(res,'fact-cont','<h3>📌 <span id="quick-facts-title">Quick Facts</span></h3>') );
generateTitle(query).then((res) =>render(res,'title-cont','','h2') )
	

	generateFood(query).then((res) =>render(res,'food-cont') );
	generateOrigin(query).then((res) =>render(res,'origin-cont') );
	
	generateTradition(query).then((res) =>render(res,'tradition-cont') );
	
generateTip(query).then((res) =>render(res,'tips-cont') );

	
}
let toDisplay=true
 function render(data,cont,title,el,) {
	if (!toDisplay) {
	return
}


	if (data.split(' ')[0].toLowerCase()=='error'||data.toLowerCase() === 'enter correct keyword') {
	document.querySelector('.main-section').innerHTML = '';
displayWarning(data)
		toDisplay=false
		
		return
	}
	
	const target = document.getElementById(cont)
	if (title) {
		target.innerHTML=title+data
		
	
	}	else if (el) {
		target.firstElementChild.remove()

		const element = document.createElement(el);
		element.innerHTML=data;
		target.append(element)
	
	} else {
		target.innerHTML=data;

	}
	try {
	target.classList.remove('skeleton');
	
} catch (e) {}
	try {
		
		target.classList.remove('title-skeleton');
	} catch (e) {}
		try {
					target.classList.remove('hide-shadow');
		} catch (e) {}	
return
}

display(query)


function displayWarning(message) {
  const main=document.querySelector('.main-section')
  main.innerHTML=''
 main.innerHTML=`<center>
 	<h3>
 		${message}
 	</h3>
 </center>`
}