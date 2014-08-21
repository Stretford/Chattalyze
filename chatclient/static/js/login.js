/**
 * Created by stretford on 8/12/14.
 */

$('#login').click(function(){
    login_info = {'username': $('#login_username').val(), 'password': $('#login_password').val()}
    $.post('/', login_info).done(function(msg){
        if(msg == 'logged in')
            window.location.href = "/index"

    })
})

$('#signup').click(function(){
    $('.modal').modal('show')
})

