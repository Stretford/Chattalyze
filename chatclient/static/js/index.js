/**
 * Created by applelab1 on 8/19/14.
 */
$(function(){
    $('#canvas').hide()
    $("#send_msg").addClass('disabled')
});

$('.chatter').click(function(){
    $('#canvas').show()
    $(this).addClass('uk-button-success')
})


$('#input').bind('input propertychange', function(){ checkempty();});

function checkempty(){
    if($('#input')[0].value != '')
    {
        $('#send_msg').removeClass('disabled')
    }
    else
    {
        $('#send_msg').addClass('disabled')
    }
}

function append_msg(username, msg){
    var time = new Date()
    var str = username + " (" + time.getHours() + ":" + time.getMinutes() + ") :" + msg
    $('#history').append("<div>" + str + "</div")

}


$('#send_msg').click(function(){
    //$('.ui.large.message').text($('.ui.large.message').text().replace('No Chatting History...', ''))
    var userid = $('#online-friends')[0].className.split('_')[2]
    var token = $('#online-friends')[0].className.split('_')[0]
    var username = $('#online-friends')[0].className.split('_')[1]
    //var time = new Date()
    //var str = username + " (" + time.getHours() + ":" + time.getMinutes() + ") :" + $('#input')[0].value
    append_msg(username, $('#input')[0].value)
    var receiver = $('.uk-button-success.chatter')[0].id
    var to = receiver.split('_')[1]
    var to_token = receiver.split('_')[0]
    /*var p = document.createElement("div")
    p.innerHTML = str
    document.getElementById('history').appendChild(p)
    //$('.ui.large.message').html($('.ui.large.message').html() + str)
    */
    //$('#history').append("<div>" + str + "</div")
    msg = {msg: $('#input')[0].value, to:to, to_token:to_token}
    $('#input')[0].value = ''
    $(this).addClass('disabled')

    $.post('/index', msg).done(function(msg){
    })
})

/*
function receive_msg(){
    //document.write('aaa')
    $.getJSON('/receive_msg', {}, function(data){
        //username = data.split('_')[0]
        //msg = data.split('_')[1]
        //append_msg(username, msg)
        $('#all-friends')[0].innerHTML += data
        //alert(data)
    });
    //setTimeout("receive_msg();", 500)
}
*/

