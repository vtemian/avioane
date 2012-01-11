$(document).ready(function(){
    var login = true;
    $('#sign-switch').click(function(){
        $('#menu_login').toggleClass('menu_login_display');
        $('#menu_reg').toggleClass('menu_reg_display');
        login = !login;
        if(login){
            $(this).html('Register!');
        }else{
            $(this).html('Login!');
        }

    });
    $('.fb_login').click(function(){
       window.location='/facebook/login';
    });
});