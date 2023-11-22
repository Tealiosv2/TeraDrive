let casesButton = document.getElementById("cases-anchor");
let detailsButton = document.getElementById("details-anchor");
let dashboardButton = document.getElementById("dashboard-anchor");

let casesNav = document.getElementById("case-nav-wrapper");
let summaryNav = document.getElementById("case-summary-wrapper");
let detailsNav = document.getElementById("case-details-wrapper");

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

function dropDownToggleCases() {
    document.getElementById("dropdown-menu-1").classList.toggle("show");
    console.log('hi');
  }

function dropDownToggleDetails() {
    document.getElementById("dropdown-menu-1").classList.toggle("show");
    console.log('hi');
  }
  
  
//   // Close the dropdown menu if the user clicks outside of it
//   window.onclick = function(event) {
//     if (!event.target.matches('.dropdown-toggle')) {
//       var dropdowns = document.getElementsByClassName("dropdown-content");
//       var i;
//       for (i = 0; i < dropdowns.length; i++) {
//         var openDropdown = dropdowns[i];
//         if (openDropdown.classList.contains('show')) {
//           openDropdown.classList.remove('show');
//         }
//       }
//     }
//   }