// All JS contained in this file will run once the page has fully loaded
$(document).ready(function () {
  // Initialize the side menu functionality
  $(".sidenav").sidenav({ edge: "right" });

  // Initialize the collapsible functionality
  $(".collapsible").collapsible();

  // Initalize the tooltips
  $(".tooltipped").tooltip();

  // Intialize the datepicker
  $(".datepicker").datepicker({
    format: "dd mmmm yyyy",
    yearRange: 3,
    showClearBtn: true,
    i18n: {
      done: "select",
    },
  });

  // Initialize the select
  $("select").formSelect();
});
