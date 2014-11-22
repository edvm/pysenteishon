// chronometer / stopwatch JS script - coursesweb.net
// Here set the minutes, seconds, and tenths-of-second when you want the chronometer to stop
// If all these values are set to 0, the chronometer not stop automatically
var stmints = 0;
var stseconds = 0;
var stzecsec = 0;

var chrRunning = false;

// the initial tenths-of-second, seconds, and minutes
var zecsec = 0;
var seconds = 0;
var mints = 0;
var startchron = 0;

// function to be executed when the chronometer stops
function toAutoStop() {
  "use strict";
  console.log("toAutoStop");
}

function chronometer() {
  "use strict";
  var timeoutID;

  if (startchron == 1) {
    zecsec += 1;       // set tenths of a second

    // set seconds
    if (zecsec > 9) {
      zecsec = 0;
      seconds += 1;
    }

    // set minutes
    if (seconds > 59) {
      seconds = 0;
      mints += 1;
    }

    // adds data in #showtm
    document.getElementById("showtm").innerHTML = mints + " : " + seconds + "<sub>" + zecsec + "</sub>";

    // if the chronometer reaches to the values for stop, calls whenChrStop(), else, auto-calls chronometer()
    if (zecsec == stzecsec && seconds == stseconds && mints == stmints) {
      toAutoStop();
    } else {
      timeoutID = window.setTimeout(chronometer, 100);
    }
  }
}

function startChr() {
  "use strict";
  chrRunning = true;
  startchron = 1;
  chronometer();  // starts the chronometer
}

function stopChr() {
  "use strict";
  chrRunning = false;
  startchron = 0;  // stops the chronometer
}

function chrIsRunning(){
  "use strict";
  return chrRunning;
}

function resetChr() {
  "use strict";
  zecsec = seconds = mints = startchron = 0;
  document.getElementById("showtm").innerHTML = mints + " : " + seconds + "<sub>" + zecsec + "</sub>";
}

// start the chronometer, delete this line if you want to not automatically start the stopwatch
// startChr();


$(function() {
  // Enable swiping...
  $("#touche").swipe({
    //Generic swipe handler for all directions
    swipe: function(event, direction, distance, duration, fingerCount, fingerData) {
      "use strict";

      // console.log("You swiped " + direction );
      var slideMsg = "";
      var url = "/btn-" + direction + "/";
      var icon = "fa fa-arrow-circle-" + direction + " fa-5x center-block";

      if (direction == "right") {
        slideMsg = "Shows previous slide!";
      } else if (direction == "left") {
        slideMsg = "Shows next slide!";
      } else if (direction == "up") {
        slideMsg = "Pressed Key Up!";
      } else if (direction == "down") {
        slideMsg = "Pressed Key Down";
      } else {
        icon = "fa fa-warning fa-5x center-block";
        slideMsg = "Not implemented option!";
      }

      $("#touche-directions-icon").attr("class", icon);
      $("#slide-text").html(slideMsg);

      $.ajax({
        type: "GET",
        url: url,
        dataType: "json"
      });
    },
    //Default is 75px, set to 0 for demo so any distance triggers swipe
    threshold:0
  });

  $(".chronometer").swipe({
    tap: function(event, object){
      if (chrIsRunning() === false) {
        startChr();
      }
    },

    doubleTap: function(event, object) {
      resetChr();
      stopChr();
    },
  });
});
