function add(e, num){
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'/add',
      data:{
         title:$("#title_"+num).val()
      },
      success:function()
      {
        alert('Reassignment Submitted.');
      }
    })
  };