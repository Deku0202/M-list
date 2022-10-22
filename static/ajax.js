function add(e, num){
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'/add',
      data:{
         title:$("#title_"+num).val()
      },
      success: function() { 
        $('.message').fadeIn('slow');
        //$('#msg').html("data insert successfully").fadeIn('slow') //also show a success message 
        $('.message').delay(3000).fadeOut('slow');
      },
      error: function () {
        console.log("error")
      }
    })
  };