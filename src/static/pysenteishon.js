$(function() {      
  //Enable swiping...
  $("#touche").swipe( {
    //Generic swipe handler for all directions
    swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
      $(this).text("You swiped " + direction );  
      var url = '/btn-' + direction + '/'
      $.ajax({
        type: 'GET',
        url: url, 
      });
    },
    //Default is 75px, set to 0 for demo so any distance triggers swipe
    threshold:0
  });
});
