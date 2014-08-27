/**
 * Created by stretford on 8/21/14.
 */

$(function(){
  var host = "ws://localhost:8888/";
  try{
    sock = new WebSocket(host);
    sock.onopen    = function(msg){ ; };
    sock.onmessage = function(msg){ log(msg.data); };
    sock.onclose   = function(msg){ log("Lose Connection!"); };
  }
  catch(ex){ alert(ex) }
    sock.send('Hi!')
})




