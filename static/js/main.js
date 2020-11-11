
$(document).ready(function () {
  $(".header_menu_open").click(function (e) { 
    e.preventDefault();

    if ($(this).find($(".fa")).attr('class')=='fa fa-bars'){
      $(this).find($(".fa")).removeClass('fa fa-bars').addClass('fa fa-times');
      $('#mobile_menu').addClass("show");
    } else {
      $(this).find($(".fa")).removeClass('fa fa-times').addClass('fa fa-bars');
      $('#mobile_menu').removeClass("show");
    }
  });

  $(".header_main_menu_sm").click(function (e) { 
    e.preventDefault();
    $("#header_main_menu_in").find($("ul")).addClass('show');
    
  });

  $(".header_menu_title").click(function (e) { 
    e.preventDefault();
    $("#header_main_menu_in").find($("ul")).removeClass('show');
  });

  $(".header_menu_head_hide").click(function (e) { 
    e.preventDefault();
    console.log('im here');
    console.log($(this).closest('li').attr('class'));
    $(this).closest('li').removeClass();
    console.log($(this).closest('li').attr('class'));
  });
  
  $(".header_main_menu>li>span").click(function (e) { 
    e.preventDefault();
    console.log('im here too');
    $(this).closest('li').addClass("hover");
    
  });
}); 
