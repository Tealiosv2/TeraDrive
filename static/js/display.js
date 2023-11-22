//buttons for each of the sections - cases, details, clients
let casesButton = document.getElementById("cases-anchor");
let detailsButton = document.getElementById("details-anchor");
let dashboardButton = document.getElementById("dashboard-anchor");

//divs for each of the sections - cases, details, clients
let casesNav = document.getElementById("case-nav-wrapper");
let summaryNav = document.getElementById("case-summary-wrapper");
let detailsNav = document.getElementById("case-details-wrapper");

//dropdown divs for each of the sections that have dropdowns(cases and details)
let casesDropdownButton = document.getElementById("dropdown-cases");
let dropdownCasesOptions = document.getElementById("dropdown-menu-cases");
let detailsDropdownButton = document.getElementById("dropdown-details");
let dropdownDetailsOptions = document.getElementById("dropdown-menu-details");

//functions to show/hide the sections
function showCases() {
    casesNav.style.display = "block";
    summaryNav.style.display = "none";
    detailsNav.style.display = "none";
}

function showDetails() {
    casesNav.style.display = "none";
    summaryNav.style.display = "none";
    detailsNav.style.display = "block";
}

function showAll() {
    casesNav.style.display = "block";
    summaryNav.style.display = "block";
    detailsNav.style.display = "block";
}

casesButton.addEventListener("click", showCases);

detailsButton.addEventListener("click", showDetails);

dashboardButton.addEventListener("click", showAll);

//Dropdown stuff, inspiration taken from https://www.w3schools.com/howto/howto_js_dropdown.asp
function dropDownToggleCases() {
  document.getElementById("dropdown-menu-cases").classList.toggle("show");
}

function dropDownToggleDetails() {
  document.getElementById("dropdown-menu-details").classList.toggle("show");
  console.log('hi');
}


//Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.cases-btn')) {
    var dropdowns = document.getElementsByClassName("dropdown-menu");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }

  if (!event.target.id.matches('.details-btn')) {
    var dropdowns = document.getElementsByClassName("dropdown-menu");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
  