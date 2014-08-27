/**
 * Created by stretford on 8/21/14.
 */

var sock;
var host = "ws://localhost:8888/";


$(function(){
  try{
    sock = new WebSocket(host);
    sock.onopen    = function(msg){ alert('OnOpen!') };
    sock.onmessage = function(msg){ document.write(msg.data) };

  }
  catch(ex){ alert(ex) }
    //sock.send('Hi!')
})

$('#send').click(function(){
    //sock.onclose   = function(msg){ alert('close') };
    sock.send('aaaaaaa!')
    //sock.close()
})



