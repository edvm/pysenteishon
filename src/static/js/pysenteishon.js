function Chronometer ($el) {
  this.$el = $el;
  this.$timeLeft = this.$el.find('.time-left');
  this.$clock = this.$el.find('.clock');
  this.running = false;
  this.lastCheckTime = null;
  this.milliSecondsLeft = 45*60*1000;

  this.notifications = [
    10,
    5
  ];

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
      this.checkNotifications();
    }
  }.bind(this), 500);

  this.render = function () {
    var min = (this.milliSecondsLeft/1000/60) << 0;
    var sec = (this.milliSecondsLeft/1000) % 60 << 0;
    sec = ('000'+Math.abs(sec)).slice(-2);
    this.$timeLeft.text(min+":"+sec);
  };

  this.checkNotifications = function () {
    // reduced by one to avoid notifying on the end 10:59
    var min = ((this.milliSecondsLeft/1000/60) << 0) - 1;
    var len = this.notifications.length;
    this.notifications = this.notifications.filter(function (time) {
      return time != min;
    });
    if ( len != this.notifications.length ) {
      // filtered notification have less items, lets notify the user
      this.notify('Time left '+min);
    }
  };

  // notify permission
  Notification.requestPermission();
  this.notify = function (text) {
    if (!('Notification' in window)) {
      return
    }
    if (Notification.permission === 'granted') {
      new Notification(text);
    }
  };

  this.render();
}


function Slider ($el) {
  this.$el = $el;
  this.doDoing = false;

  this.do = function (key) {
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
  };

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


$(function () {
  var chronometer = new Chronometer($('#chronometer'));
  var slider = new Slider($('#slider'));
  var networkInfo = new NetworkInfo($('#network-info'));
});
