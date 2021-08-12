// All JS contained in this file will run once the page has fully loaded
$(document).ready(function () {

  // Initialize the side menu functionality
  $(".sidenav").sidenav({edge: "right"});

  // Initialize the collapsible functionality
  $('.collapsible').collapsible();

  // Initalize the tooltips
  $('.tooltipped').tooltip();
});

