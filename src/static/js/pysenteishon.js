$(function() {      
  //Enable swiping...
  $("#touche").swipe({
    //Generic swipe handler for all directions
    swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
      // $(this).text("You swiped " + direction );
      var icon = '<i class="fa fa-arrow-circle-' + direction + ' fa-5x center-block"></i>';
      $('#touche-directions').html(icon);
     if ( direction == 'right' ) {
        $('#slide-msg h3').html('Shows previous slide!')
      } else if ( direction == 'left' ) {
        $('#slide-msg h3').html('Shows next slide!')
      } else if ( direction == 'up' ) {
        $('#slide-msg h3').html('Pressed Key Up!')
      } else if ( direction == 'down' ) {
        $('#slide-msg h3').html('Pressed Key Down')
      } else {
        var icon = '<i class="fa fa-warning fa-5x center-block"></i>';
        $('#touche-directions').html(icon);
        $('#slide-msg h3').html('Not implemented option!')
      }
      var url = '/btn-' + direction + '/'
      $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json'
      });
    },
    //Default is 75px, set to 0 for demo so any distance triggers swipe
    threshold:0
  });
});
