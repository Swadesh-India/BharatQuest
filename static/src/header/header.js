let m = document.querySelector(".menu-cont");
let c = false;
document.getElementById("menu").addEventListener("click", (e) => {
  switchidden(true);
});
function switchidden(isMenu) {
  c = !c;
  
    c ? m.setAttribute("id", "menu-show") : m.removeAttribute("id");
  
}
let fs =
  parseInt(
    getComputedStyle(document.querySelector(".home-header")).fontSize.trim(
      "px",
    ),
  ) * 3;


function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return rect.top <= window.innerHeight;
}
const toggleContainer = Array.from(
  document.querySelectorAll(".toggle-container"),
);
toggleContainer.forEach((cont) => {
  const ball = cont.children[0].children[1];

  let height = getDimension(cont, "height");
  let width = getDimension(cont, "width");

  setOrientation(cont, ball, height, width);
});
const modeSwitcherBall =
  document.querySelector(".toggle-container").children[0].children[1];

// window.onload=(e) => {

let height = getDimension(
  modeSwitcherBall.parentElement.parentElement,
  "height",
);
let width = getDimension(modeSwitcherBall.parentElement.parentElement, "width");


if (localStorage.getItem("darkMode") == "true") {
  document.body.classList.add("dark");
  modeSwitcherBall.style.left = `${(width / 100) * 95.8 - getDimension(modeSwitcherBall, "height")}px `;
} else {
  document.body.classList.remove("dark");
  modeSwitcherBall.style.left = `${(height / 100) * 7.5}px`;
}

// }

function getDimension(target, axis) {
  return parseInt(getComputedStyle(target).getPropertyValue(axis).slice(0, -2));
}

let on = 0;
function setOrientation(toggleContainer, ball, height, width) {
  ball.style.width =
    ball.style.height = `${(getDimension(toggleContainer, "height") / 100) * 85}px`;

  toggleContainer.children[0].style.alignItems = "center";
  toggleContainer.style.borderRadius = `${height / 2}px`;
  ball.style.left = `${(height / 100) * 7.5}px`;

  toggleContainer.addEventListener("click", (e) => {
    e.preventDefault();
    if (ball == modeSwitcherBall) {
      switchMode();
      ball.style.left =
        localStorage.getItem("darkMode") == "true"
          ? `${(width / 100) * 95.8 - getDimension(ball, "height")}px `
          : `${(height / 100) * 7.5}px`;
    } else {
      ball.style.left =
        toggleContainer.dataset.notif == "true"
          ? `${(width / 100) * 95.8 - getDimension(ball, "height")}px `
          : `${(height / 100) * 7.5}px`;
    }

    on++;
  });

  if (
    ball != document.querySelector(".toggle-container").children[0].children[1]
  ) {
    ball.style.left =
      toggleContainer.dataset.notif == "true"
        ? `${(width / 100) * 95.8 - getDimension(ball, "height")}px `
        : `${(height / 100) * 7.5}px`;
  }
}

function switchMode() {
  let darkMode;
  try {
    darkMode = localStorage.getItem("darkMode");
  } catch (e) {
    localStorage.setItem("darkMode", "false");
    darkMode = localStorage.getItem("darkMode");
  }
  if (darkMode == "true") {
    document.body.classList.remove("dark");
    localStorage.setItem("darkMode", "false");
  } else {
    document.body.classList.add("dark");
    localStorage.setItem("darkMode", "true");
  }
}

console.log(
  "%cWelcome to BharatQuest!",
  "color: #fff; background:#5350c4;border-radius:6px;padding:0.5em;font-size: 20px; font-weight: bold;",
);

const profileBtn1 = Array.from(
  document.getElementsByClassName("profile-wrapper"),
)[0];
const profileBtn2 = document.getElementsByClassName("profile-wrapper-hum")[0];
if (profileBtn1 && profileBtn2) {
  profileBtn1.addEventListener("click", (e) => {
  showProfile();
});
profileBtn2.addEventListener("click", (e) => {
  showProfile();
});



const profile = document.getElementById("profile");
function showProfile() {


  if (profile) {
    profile.style.display = "flex";
  }
}

const closePrBtn = document.getElementById("close-profile");
closePrBtn.addEventListener("click", (e) => {
  if (profile) {
    profile.style.display = "none";
  }
  closeProfile();

});


const profileLinks = Array.from(
  document.querySelectorAll(".profile-options-container ul>li"),
).filter((el) => el.dataset.redirecturl != "#");
profileLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    location.href = link.dataset.redirecturl;
  });
});

const profileLinksMove = Array.from(
  document.querySelectorAll(".profile-options-container ul>li"),
).filter((el) => el.dataset.redirecturl == "#");
const profileAside = document.querySelector(".profile-aside");
const profileMain = document.querySelector(".profile-main-wrapper");
profileLinksMove.forEach((link) => {
  const svg = link.querySelector(".arrow-svg");

  link.addEventListener("click", (e) => {
    e.preventDefault();
    linkedTab = link.dataset.linkedtab;

    toggleProfile(svg, linkedTab);
  });
});
function closeProfile() {
  // 1. Reset everything (covers both mobile and desktop states)
  profileAside.style.transform = "translateX(0)";
  profileMain.style.transform = "translateX(0)";
  profileAside.style.opacity = "0";

  // Reset z-index just to keep the DOM clean when closed
  profileAside.style.zIndex = "1";

  // 2. Find all arrow SVGs inside #profile and derotate them
  const allArrows = document.querySelectorAll("#profile .arrow-svg");
  allArrows.forEach((svg) => {
    svg.style.transform = "rotate(0deg)";
    const rotatable = document.querySelector(".rotatable");
    if (rotatable) {
      rotatable.classList.remove("rotate");
    }
  });

  // 3. Wait for the CSS fade transition (300ms) to finish before hiding it
  setTimeout(() => {
    profileAside.style.display = "none";
  }, 300);
}

function toggleProfile(svg, linkedTab) {
  const isClosed = getComputedStyle(profileAside).display === "none";
  const rotatable = document.querySelector(".rotatable");
  if (isClosed) {
    toggleTab(linkedTab, true);

    profileAside.style.display = "flex";

    setTimeout(() => {
      const isMobile = window.innerWidth <= 768;

      if (isMobile) {
        profileAside.style.transform = "translate(0, 0)";
        profileMain.style.transform = "translate(0, 0)";

        // Bring the aside to the front
        profileAside.style.zIndex = "50";
      } else {
        // ==========================================
        // DESKTOP: Horizontal Slide
        // ==========================================
        profileAside.style.transform = "translateX(50%)";
        profileMain.style.transform = "translateX(-50%)";

        // Reset z-index to default for desktop layout
        profileAside.style.zIndex = "1";
      }

      // Apply common styles (fade in and rotate)
      profileAside.style.opacity = "1";

      if (svg) {
        svg.style.transform = "rotate(180deg)";
      }
    }, 10);
    if (rotatable) {
      rotatable.classList.add("rotate");
    }
  } else {
    toggleTab(linkedTab, false);

    closeProfile();
  }
}

const closeAsideBtn = document.querySelector(".close-aside-btn");

closeAsideBtn.addEventListener("click", (e) => {
  closeProfile();
});

function toggleTab(linkedTab, toOpen) {
  const asideMain = Array.from(
    document.querySelectorAll(".profile-aside-main"),
  );

  asideMain.forEach((el) => {
    el.style.display = "none";
  });
  if (toOpen) {
    tabToOpen = asideMain.filter((el) => el.dataset.linkedtab == linkedTab)[0];
    tabToOpen.style.display = "block";
  }
}
}