function tester(clicked)
{
	console.log(clicked)
	var audio = document.getElementById('player');
	$('audio').remove();
	document.getElementById('hearME').innerHTML = '<audio controls id="player" autoplay></audio>';
	audio = document.getElementById('player');
	audio = $("audio").get(0);
	document.getElementById(clicked);
    var songN = clicked.innerHTML;
	audio.src = songN;
	$("#player").attr("src","/static/songs/"+songN+".mp3");
	var old = document.getElementById('other').innerHTML;
	var currentdate = new Date(); 
    var datetime = "" + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + ", at: "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
	document.getElementById('other').innerHTML = old+'<p>On the '+datetime+', you played: >>> <a class="history" onclick="tester(this)">'+songN+'</a> <<< click to play again.</p>';
	$(songN).appendTo('#other')
}

window.setInterval(function()
{

    console.log("working")
}, 5000);