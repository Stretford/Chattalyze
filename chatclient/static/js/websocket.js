/**
 * Created by applelab1 on 8/28/14.
 */

var socket;

function init(){
  var host = "ws://localhost:8888/";
  try{
    socket = new WebSocket(host);
    socket.onopen    = function(msg){ socket.send('2') };
    socket.onmessage = function(msg){ log(msg.data); };
    socket.onclose   = function(msg){ log("Lose Connection!"); };

  }
  catch(ex){ log(ex); }
}

function send(){
    var userid = $('#online-friends')[0].className.split('_')[2]
    var token = $('#online-friends')[0].className.split('_')[0]
    var username = $('#online-friends')[0].className.split('_')[1]
    //var time = new Date()
    //var str = username + " (" + time.getHours() + ":" + time.getMinutes() + ") :" + $('#input')[0].value
    append_msg(username, $('#input')[0].value)
    var receiver = $('.uk-button-success.chatter')[0].id
    var to = receiver.split('_')[1]
    var to_token = receiver.split('_')[0]

    //$('#history').append("<div>" + str + "</div")
    msg = {msg: $('#input')[0].value, to:to, to_token:to_token}
    $('#input')[0].value = ''
    $(this).addClass('disabled')

  try{ socket.send(msg); } catch(ex){ log(ex); }
  $.post('/index', msg).done(function(msg){
    })
}


//$('.ui.large.message').text($('.ui.large.message').text().replace('No Chatting History...', ''))


    //$.post('/index', msg).done(function(msg){
    //})

window.onbeforeunload=function(){
    try{
        socket.send('quit');
        socket.close();
        socket=null;
    }
    catch(ex){
        log(ex);
    }
};


//function $(id){ return document.getElementById(id); }
function log(msg){ $('#history')[0].innerHTML+="<br>"+msg; }
function onkey(event){ if(event.keyCode==13){ send(); } }