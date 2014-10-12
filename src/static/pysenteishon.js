$(function() {      
  //Enable swiping...
  $("#touche").swipe({
    //Generic swipe handler for all directions
    swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
      $(this).text("You swiped " + direction );  
      var url = '/btn-' + direction + '/'
      $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        statusCode: {
          500: function(jqXHR, textStatus, errorThrown){
            show_error_modal(title='Internal server error', body=textStatus, show=true);
          }
        },
        success: function ( data, textStatus, jqXHR ){
          if ( data.status == false ){
            show_error_modal(title='Error', titleIcon='warning', body=data.msg, show=true);
          }
        }
      });
    },
    //Default is 75px, set to 0 for demo so any distance triggers swipe
    threshold:0
  });

  // utilities
  function show_error_modal (title='', titleIcon=false, body='', show=false) {
    if ( titleIcon !== false )
      title = '<i class="fa fa-' + titleIcon + '">' + ' ' + title;
    $('#error-modal .modal-title').html(title);
    $('#error-modal .modal-body').html(body);
    if ( show === true ){
      $('#error-modal').modal();
    }
  }
});
