function Chronometer ($el) {
  this.$el = $el;
  this.$timeLeft = this.$el.find(".time-left");
  this.$clock = this.$el.find(".clock");
  this.running = false;
  this.lastCheckTime = null;
  this.milliSecondsLeft = 45*60*1000;

  this.$clock.swipe({
    tap: function (event, object) {
      this.running = !this.running;
      if (this.running) {
        this.$timeLeft.css("color", "green");
        this.lastCheckTime = new Date();
      } else {
        this.$timeLeft.css("color", "red");
      }
    }.bind(this),
    doubleTap: function(event, object) {
    }
  });

  this.$timeLeft.click(function(){
    var minutes = prompt("Time in minutes");
    this.milliSecondsLeft = minutes*60*1000;
    this.lastCheckTime = new Date();
    this.running = false;
    this.render();
  }.bind(this));

  setInterval(function () {
    if (this.running) {
      this.milliSecondsLeft -= ((new Date()).getTime() - this.lastCheckTime.getTime());
      this.lastCheckTime = new Date();
      this.render();
    }
  }.bind(this), 500);

  this.render = function () {
    var min = (this.milliSecondsLeft/1000/60) << 0;
    var sec = (this.milliSecondsLeft/1000) % 60 << 0;
    this.$timeLeft.text(min+":"+sec);
  };

  this.render();
}

$(function() {
  new Chronometer($("#chronometer"));

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

});
