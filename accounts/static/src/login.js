

function value(id) {
    let target = document.getElementById(id);
    if (!target) {
        console.warn('NO ELEMENT WITH ID : ', id, ' found')
        return
    }
    return target.value;
};

//function to generate captcha 
function generateCaptcha(length) {
    let captcha = '';
    let alphabet = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890';
    for (var i = 0; i < length; i++) {
        let rand = Math.floor(1 + alphabet.length * Math.random());
        captcha += ` ${alphabet[rand === alphabet.length ? alphabet.length-1 : rand]}`;
    }

    return captcha;
}



const passCheckBox = document.getElementsByClassName('hidePassword');

Array.from(passCheckBox).forEach(box => box.addEventListener('click', hidePassword));

function hidePassword(e) {
	
    
	const passInput = e.target.parentElement.parentElement.children[2];

	if (passInput.tagName != 'INPUT') {
		console.warn('inout box not found')
		return
	}
	if (passInput.type === 'password') {
		passInput.type = 'text';
	

	} else if (passInput.type === 'text') {
		passInput.type = 'password'
		

	}

}


