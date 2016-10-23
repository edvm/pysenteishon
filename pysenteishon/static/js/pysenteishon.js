function Chronometer ($el) {
  this.$el = $el;
  this.$timeLeft = this.$el.find('.time-left');
  this.$clock = this.$el.find('.clock');
  this.running = false;
  this.lastCheckTime = null;
  this.milliSecondsLeft = 45*60*1000;

  this.$clock.click(function () {
    this.running = !this.running;
    if (this.running) {
      this.$timeLeft.addClass('running');
      this.lastCheckTime = new Date();
    } else {
      this.$timeLeft.removeClass('running');
    }
  }.bind(this));

  this.$timeLeft.click(function(){
    var minutes = prompt('Time in minutes');
    if (minutes===null) { return }
    this.milliSecondsLeft = minutes*60*1000;
    this.lastCheckTime = new Date();
    this.running = false;
    this.render();
  }.bind(this));

  setInterval(function () {
    // tick
    if (this.running) {
      this.milliSecondsLeft -= ((new Date()).getTime() - this.lastCheckTime.getTime());
      this.lastCheckTime = new Date();
      this.render();
    }
  }.bind(this), 500);

  this.render = function () {
    var min = (this.milliSecondsLeft/1000/60) << 0;
    var sec = (this.milliSecondsLeft/1000) % 60 << 0;
    sec = ('000'+Math.abs(sec)).slice(-2);
    this.$timeLeft.text(min+":"+sec);
  };

  this.render();
}


function press (key) {
    if (this.doDoing) { return }
    this.doDoing = true;
    $.ajax({
      url: "/press",
      data: {
        "key": key
      },
      cache: false
    }).always(function () {
      this.doDoing = false;
    }.bind(this));
}


function Slider ($el) {
  this.$el = $el;
  this.doDoing = false;

  this.do = function(key) {press(key)};

  this.$el.find('#key-left').click(function () {
    this.do("left");
  }.bind(this));

  this.$el.find('#key-right').click(function () {
    this.do("right");
  }.bind(this));

  this.$el.find('#key-down').click(function () {
    this.do("down");
  }.bind(this));

  this.$el.find('#key-up').click(function () {
    this.do("up");
  }.bind(this));
}


function NetworkInfo ($el) {
  var $list = $el.find('.network-list ul');
  var $qr = $el.find('.network-qr');
  $.get('/ifconfig').done(function(ifconfig){
    for (var i = 0; i < ifconfig.length; i++) {
      var config = ifconfig[i];
      for (var j = 0; j < config.addresses.length; j++) {
        var $config = $('<li><span>' + config.name + ':</span>' + config.addresses[j] + '<i class="fa fa-qrcode"></i></li>');
        $config.data('name', config.name);
        $config.data('address', config.addresses[j]);
        $list.append($config);
      }
    }
  });

  $list.on('click', 'li', function (e) {
    var $li = $(this);
    $qr.fadeOut(200);
    setTimeout(function(){
      $qr.html("");
      new QRCode($el.find('.network-qr')[0], {
        text: 'http://'+$li.data('address')+":"+window.location.port,
        width: 300,
        height: 300,
        colorDark : "#366D9D",
        colorLight : "#ffffff"
      });
      $qr.delay(150).fadeIn(200);
    }, 220);
  });

}


function Swipe ($el) {
  this.$el = $el;
  this.$el.swipe({
    swipe: function(event, direction, distance, duration, fingerCount, fingerData) {
      press(direction);
    },
    fingers: 1
  });
}

function TouchPad ($touchpad) {
  var promise = $.Deferred().promise();
  function mouseMove(offset_x, offset_y){
      if (this.moving) {
        return promise
      }
      this.moving = true;
      return $.ajax({
        url: "/mouse_move",
        data: {
          "offset_x": parseInt(offset_x),
          "offset_y": parseInt(offset_y)
        },
        cache: false
      }).always(function () {
        this.moving = false;
      }.bind(this));
  }

  function mouseClick (){
      if (this.doing) { return }
      this.doing = true;
      return $.ajax({
        url: "/click",
        cache: false
      }).always(function () {
        this.doing = false;
      }.bind(this));
  }

  var start_posx = 0;
  var start_posy = 0;
  var current_posx = 0;
  var current_posy = 0;

  $touchpad.on("touchstart", function(e){
    start_posx = e.originalEvent.touches[0].pageX;
    start_posy = e.originalEvent.touches[0].pageY;
    current_posx = start_posx;
    current_posy = start_posy;
  });

  $touchpad.on("touchend", function(e){
    if ((current_posx - start_posx + current_posx - start_posx) == 0) {
      mouseClick()
    } else {
      mouseMove(
        current_posx - start_posx,
        current_posy - start_posy
      )
    }
  });

  $touchpad.on("touchmove", function(e){
    e.preventDefault(); // prevent scroll on mobile screens
    current_posx = e.originalEvent.touches[0].pageX;
    current_posy = e.originalEvent.touches[0].pageY;
    var last_posx = current_posx;
    var last_posy = current_posy;
    mouseMove(
      current_posx - start_posx,
      current_posy - start_posy
    ).done(function(){
        start_posx = last_posx;
        start_posy = last_posy;
    })
  });
}

$(function () {
  var chronometer = new Chronometer($('#chronometer'));
  var slider = new Slider($('#slider'));
  var networkInfo = new NetworkInfo($('#network-info'));
  var swipe = new Swipe($('#slider'));
  var touchPad = new TouchPad($('#touchpad'));

  var noSleep = new NoSleep();

  var wakeLockEnabled = false;
  var toggleEl = document.querySelector("#toggle");
  toggleEl.addEventListener('click', function() {
    if (!wakeLockEnabled) {
      noSleep.enable(); // keep the screen on!
      wakeLockEnabled = true;
      toggleEl.value = "Screen won't turn off";
    } else {
      noSleep.disable(); // let the screen turn off.
      wakeLockEnabled = false;
      toggleEl.value = "Screen will turn off";
    }
  }, false);

});
