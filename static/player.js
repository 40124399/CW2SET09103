function tester(clicked)
{
	var audio = document.getElementById('player');
	$('audio').remove();
	document.getElementById('hearME').innerHTML = '<audio controls id="player" preload="metadata"></audio>';
	audio = document.getElementById('player');
	audio = $("audio").get(0);
	document.getElementById(clicked);
    var songN = clicked.innerHTML;
	audio.src = songN;
	$("#player").attr("src","/static/songs/"+songN+".mp3");		
}

window.setInterval(function()
{

    console.log("working")
}, 5000);