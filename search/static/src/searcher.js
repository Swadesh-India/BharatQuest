// ===== ELEMENTS =====
const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById("search-input");
const suggestionBox = document.getElementById("suggestion-box");
const recentContainer = document.getElementById("recent-container");

if (urlParams.get('query')) {
    searchInput.value=urlParams.get('query')
}

// ===== SUGGESTIONS DATA =====
const allSuggestions = [
    "Diwali", "Holi", "Taj Mahal", "Qutub Minar", "Ajanta Caves",
    "Bihu Festival", "Garba", "Kathakali", "Pongal", "Konark Temple",
    "Rajasthani Cuisine", "Warli Art", "Ganga Aarti", "Charminar",
    "Dhokra Art", "Kumbh Mela"
];

// ===== DEFAULT POPULAR ITEMS =====
const defaultPopular = [
    "Diwali", "Taj Mahal", "Holi",
    "Kathakali", "Pongal", "Ajanta Caves"
];

// ===== LOAD RECENT SEARCHES =====
function loadRecent() {
    const recent = JSON.parse(localStorage.getItem("recent")) || [];

    recentContainer.innerHTML = "";

    if (recent.length === 0) {
        // Show default items instead
        defaultPopular.forEach(item => {
            addTag(item);
        });
        return;
    }

    recent.forEach(item => addTag(item));
}

// Create tag chip
function addTag(text) {
    const chip = document.createElement("div");
    chip.className = "tag";
    chip.innerText = text;

    chip.onclick = () => {
        searchInput.value = text;
    };

    recentContainer.appendChild(chip);
}

loadRecent();

// ===== LIVE SUGGESTIONS =====
searchInput.addEventListener("input", () => {
    const value = searchInput.value.toLowerCase();
    suggestionBox.innerHTML = "";

    if (!value) {
        suggestionBox.style.display = "none";
        return;
    }

    const filtered = allSuggestions.filter(s =>
        s.toLowerCase().includes(value)
    );

    if (filtered.length === 0) {
        suggestionBox.style.display = "none";
        return;
    }

    filtered.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        li.onclick = () => selectSuggestion(item);
        suggestionBox.appendChild(li);
    });

    suggestionBox.style.display = "block";
});

// ===== SELECT SUGGESTION =====
function selectSuggestion(text) {
    searchInput.value = text;
    suggestionBox.style.display = "none";
    saveRecent(text);
}

// ===== SAVE RECENT SEARCH =====
function saveRecent(text) {
    let recent = JSON.parse(localStorage.getItem("recent")) || [];

    // Remove duplicates
    recent = recent.filter(item => item !== text);

    // Add on top
    recent.unshift(text);

    // Limit to 8
    if (recent.length > 8) recent.pop();

    localStorage.setItem("recent", JSON.stringify(recent));
    loadRecent();
}
