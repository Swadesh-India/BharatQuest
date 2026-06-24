

const form = document.getElementById('login-form');

const passwordInput = document.getElementById('password') || document.getElementById('new_password');
const cnfPasswordInput = document.getElementById("confirm-password") ||document.getElementById("confirm_new_password")
class Validator {
    constructor() {}

    isOnlyCharOrNum(str) {
        return /^[A-Za-z0-9]+$/.test(str);
    }

    
    isNameWithSpaces(str) {
        return /^[A-Za-z\s]+$/.test(str);
    }

    // Checks if the string contains absolutely no spaces
    hasNoSpace(str) {
        return !/\s/.test(str);
    }

    validatePassword(password) {
        return {
            isLengthValid: password.length >= 8,
            hasUppercase: /[A-Z]/.test(password),
            hasLowercase: /[a-z]/.test(password),
            hasDigit: /[0-9]/.test(password),
            hasSpecial: /[@$!%*?&]/.test(password)
        };
    }
}

const validator = new Validator(); 
form.addEventListener('submit', (e) => {
    e.preventDefault(); // Always stop default submission first

    // 1. Grab your target error elements from the DOM
    const errorContainer = document.getElementById('frontend-error-container');
    const errorList = document.getElementById('frontend-error-list');
    const errorHeading = document.getElementById('error-box-heading');

    // 2. Reset the box state completely (clears out any old frontend or backend errors)
    errorList.innerHTML = "";
    errorContainer.style.display = "none";
    if (errorHeading) {
        errorHeading.textContent = "Please correct the following:";
    }

    const errors = [];

    const passwordValue = passwordInput.value; // Remeber: Don't trim passwords
    const cnfPasswordValue = cnfPasswordInput.value;

    const status = validator.validatePassword(passwordValue);
    
    if (!status.isLengthValid) {
        errors.push("Password must be at least 8 characters long.");
    }
    if (!status.hasUppercase || !status.hasLowercase) {
        errors.push("Password must contain both uppercase and lowercase letters.");
    }
    if (!status.hasDigit) {
        errors.push("Password must contain at least one number.");
    }
    if (!status.hasSpecial) {
        errors.push("Password must contain at least one special character (@$!%*?&).");
    }

    // --- PASSWORD MATCH VALIDATION ---
    if (passwordValue !== cnfPasswordValue) {
        errors.push("Passwords do not match. Please try again.");
    }

    // 4. CHECK THE ARRAY STATE
    if (errors.length > 0) {
        // Validation Failed! Loop over array and append list items dynamically
        errors.forEach((errorMessage) => {
            const li = document.createElement('li');
            li.textContent = errorMessage;
            errorList.appendChild(li);
        });

        // Make the container visible smoothly
        errorContainer.style.display = "block";
        
    refreshOverlayHeight()
    } else {

        console.log("All frontend checks passed! Submitting form...");
        form.submit();
    }
});

   const hiddenOverlay = document.querySelector('.hidden');
function refreshOverlayHeight() {
 
    if (!hiddenOverlay) return; // Guard clause

    // 1. Check current computed display state
    const isHidden = window.getComputedStyle(hiddenOverlay).display === 'none';

    if (isHidden) {
        // If it's hidden, calculate full page height and show it
        hiddenOverlay.style.height = `${document.body.scrollHeight}px`;
        hiddenOverlay.style.display = 'block';
    } else {
        // If it's already visible, hide it
        hiddenOverlay.style.display = 'none';
    }
}



const closeErrBtn = document.getElementById('close-error-box');

closeErrBtn.addEventListener('click', (e) => {
 
    e.target.parentElement.style.display="none"
       e.target.parentElement.children[2].innerHTML=""
hiddenOverlay.style.display="none"
});
