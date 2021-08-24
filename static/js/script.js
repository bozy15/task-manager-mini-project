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

  // Validates the Options dropdown in add_task.html
  /*
  * Two Varibles are created to match materialize's validation
  * If any select element has the the required attribute,
  * then we display them on the DOM but make them hidden with CSS
  * Using parent and child selectors, we check if any focused input,
  * either has or doesn't have ".disabled" class and then assign it the right variable 
  * 
  */
  validateMaterializeSelect();
  function validateMaterializeSelect() {
    let classValid = {
      "border-bottom": "1px solid #4caf50",
      "box-shadow": "0 1px 0 0 #4caf50",
    };
    let classInvalid = {
      "border-bottom": "1px solid #f44336",
      "box-shadow": "0 1px 0 0 #f44336",
    };
    if ($("select.validate").prop("required")) {
      $("select.validate").css({
        display: "block",
        height: "0",
        padding: "0",
        width: "0",
        position: "absolute",
      });
    }
    $(".select-wrapper input.select-dropdown")
      .on("focusin", function () {
        $(this)
          .parent(".select-wrapper")
          .on("change", function () {
            if (
              $(this)
                .children("ul")
                .children("li.selected:not(.disabled)")
                .on("click", function () {})
            ) {
              $(this).children("input").css(classValid);
            }
          });
      })
      .on("click", function () {
        if (
          $(this)
            .parent(".select-wrapper")
            .children("ul")
            .children("li.selected:not(.disabled)")
            .css("background-color") === "rgba(0, 0, 0, 0.03)"
        ) {
          $(this).parent(".select-wrapper").children("input").css(classValid);
        } else {
          $(".select-wrapper input.select-dropdown").on(
            "focusout",
            function () {
              if (
                $(this)
                  .parent(".select-wrapper")
                  .children("select")
                  .prop("required")
              ) {
                if (
                  $(this).css("border-bottom") != "1px solid rgb(76, 175, 80)"
                ) {
                  $(this)
                    .parent(".select-wrapper")
                    .children("input")
                    .css(classInvalid);
                }
              }
            }
          );
        }
      });
  }
});
