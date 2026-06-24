const API_KEY = 'AIzaSyD2eOe2DSokcqh7tc4QIxPXFz2csI-cYdM';

async function generateData(prompt) {
	const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=${API_KEY}`
	const requestOptions = {
		'method': 'POST',
		'headers': {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			"contents": [{
				"parts": [{ "text": prompt }]
		}]
	})
}
	try {


		const response = await fetch(API_URL, requestOptions);
		const data = await response.json();
		
		if (!response.ok) throw new Error(`Error Code : ${data.error.code} <br> Message : ${data.error.message}`);
  
		const answer = data.candidates[0].content.parts[0].text
		return answer.replace(/^###\s*(.+)$/gm, "<h3>$1</h3>");

	} catch (e) {
	  
		return e.message
		
	};
}

export {generateData};