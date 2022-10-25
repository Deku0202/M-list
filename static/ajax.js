function add(e, num){
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'/add',
      data:{
         title:$("#title_"+num).val()
      },
      success: function() { 
        $('.200').fadeIn('slow');
        $('.200').delay(3000).fadeOut('slow');
      },
      error: function () {
        $('.400').fadeIn('slow');
        $('.400').delay(3000).fadeOut('slow');
      }
    })
  };