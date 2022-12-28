function add(e, num){
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'/add',
      data:{
         title:$("#title_"+num).val(),
        //  name:$("#name_"+num).val(),
        //  date:$("#date_"+num).val(),
        //  type:$("#type_"+num).val(),
        //  img:$("#img_"+num).val()
      },
      success: function() { 
        $('.200').fadeIn('slow');
        $('.200').delay(3000).fadeOut('slow');
        $.ajax({
          type:'POST',
          url:'/added',
          data:{
            title:$("#title_"+num).val(),
            name:$("#name_"+num).val(),
            date:$("#date_"+num).val(),
            type:$("#type_"+num).val(),
            img:$("#img_"+num).val()
          }
        })
      },
      error: function () {
        $('.400').fadeIn('slow');
        $('.400').delay(3000).fadeOut('slow');
      }
    })
  };

function chgpass(e){
  e.preventDefault();
  $.ajax({
    type:'POST',
    url:'/chgpass',
    data:{
      newpass:$("#password").val(),
      confirmpass:$("#confirm").val()
    },
    success: function() { 
      $('.200').fadeIn('slow');
      $('.200').delay(3000).fadeOut('slow');
    },
    error: function (jqXHR) {
      if (jqXHR.status == 401)
      {
        $('.400').fadeIn('slow');
        $('.400').delay(3000).fadeOut('slow');
      }
      else if (jqXHR.status == 402)
      {
        $('.500').fadeIn('slow');
        $('.500').delay(3000).fadeOut('slow');
      }
    }
  })
};