let casesButton = document.getElementById("cases-anchor");
let detailsButton = document.getElementById("details-anchor");
let dashboardButton = document.getElementById("dashboard-anchor");
let clientsButton = document.getElementById("clients-anchor");

let casesNav = document.getElementById("case-nav-wrapper");
let detailsNav = document.getElementById("case-details-wrapper");
let clientsNav = document.getElementById("clients-nav-wrapper");

let casesDropdownButton = document.getElementById("dropdown-cases");
let dropdownCasesOptions = document.getElementById("dropdown-menu-cases");
let detailsDropdownButton = document.getElementById("dropdown-details");
let dropdownDetailsOptions = document.getElementById("dropdown-menu-details");

function showCases() {
    casesNav.style.display = "block";
    detailsNav.style.display = "none";
    clientsNav.style.display = "none";
    console.log('hi');
}

function showDetails() {
    casesNav.style.display = "none";
    detailsNav.style.display = "block";
    clientsNav.style.display = "none";
    console.log('hi');
}

function showAll() {
    console.log(casesNav.style.display);

    casesNav.style.display = "block";
    detailsNav.style.display = "block";
    clientsNav.style.display = "block";
}

function showClients() {
    casesNav.style.display = "none";
    detailsNav.style.display = "none";
    clientsNav.style.display = "block";
    console.log('hi');
}

dashboardButton.addEventListener("click", showAll);

casesButton.addEventListener("click", showCases);

detailsButton.addEventListener("click", showDetails);

clientsButton.addEventListener("click", showClients);

function dropDownToggleCases() {
  document.getElementById("dropdown-menu-cases").classList.toggle("show");
}

function dropDownToggleDetails() {
  document.getElementById("dropdown-menu-details").classList.toggle("show");
}


// Close the dropdown menu if the user clicks outside of it
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

  if (!event.target.matches('.details-btn')) {
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