$(function() {      
  //Enable swiping...
  $("#touche").swipe( {
    //Generic swipe handler for all directions
    swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
      $(this).text("You swiped " + direction );  
      if (direction == 'right'){
          $.ajax({
            type: 'GET',
            url: '/btn-right/',
          });
      }
      if (direction == 'left'){
          $.ajax({
            type: 'GET',
            url: '/btn-left/',
          });
      }
      if (direction == 'up'){
          $.ajax({
            type: 'GET',
            url: '/btn-up/',
          });
      }
      if (direction == 'down'){
          $.ajax({
            type: 'GET',
            url: '/btn-down/',
          });
      }
    },
    //Default is 75px, set to 0 for demo so any distance triggers swipe
      threshold:0
  });
});
