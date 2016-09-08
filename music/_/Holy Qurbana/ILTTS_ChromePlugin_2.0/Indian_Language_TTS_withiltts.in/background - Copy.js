var seltext = null;

function playsound(){
//alert("from play");
    var snd=document.getElementById('noise');
    //snd.src="Kalimba.mp3";
	snd.src="http://tts.cdacmumbai.in/wav_output/fest_out99830895.mp3"
    snd.load();
    snd.play();
}
function pausesound(){
    var snd=document.getElementById('noise');
    snd.pause();
}
	
chrome.extension.onMessage.addListener(
    function(request, sender, sendResponse) 
	{
	//alert("from background.js");
        switch (request.directive) {
        case "play":
			alert("click received for "+request.directive+" "+seltext);
            playsound();
            break;
		case "pause":
			//alert("click received for "+request.directive);
            pausesound();
            break;
        default:
            // helps debug when request directive doesn't match
            alert("Unmatched request of '" + request + "' from script to background.js from " + sender);
        }
    }
);

 
chrome.extension.onRequest.addListener(function(request, sender, sendResponse)
{
    switch(request.message)
    {
        case 'setText':
            window.seltext = request.data;
			//alert("from bg===>"+seltext);
        break;
         
        default:
            sendResponse({data: 'Invalid arguments'});
        break;
    }
});
 
 
function send_req()
{
var url = "http://tts.cdacmumbai.in/festival_cs_plugin.php";
     
        
//var url = "http://localhost/tts/festival_cs_plugin.php";
 
  	//nitech_us_rms_arctic_hts - American Male 1
  	//nitech_us_bdl_arctic_hts - American Male 2
  	//nitech_us_slt_arctic_hts - American Female
  	//nitech_us_awb_arctic_hts - Scottish Male
  	//var params = "speech="+selText+"&voice="+vc+"&volume_scale=5&make_audio=Convert Text To Speech";   
    var count =  Math.floor( Math.random()*100000000 +1 );
    //window.alert("count="+count);
      var params = "Languages="+lang+"&voice="+vc+"&ex=execute&op="+selText+"&count="+count;  
     // window.alert(params);     
  	http = new XMLHttpRequest();
  	http.open("POST", url, true);
  	//Send the proper header information along with the request
  	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  	http.setRequestHeader("Content-length", params.length);
  	http.setRequestHeader("Connection", "close");
  	http.onreadystatechange = function() {
		if(http.readyState == 4) {
			var resTxt = http.responseText;
                        //window.alert("resTxt="+resTxt);
			var startTxt = resTxt.indexOf("temp/");
                       //var startTxt = resTxt.indexOf("wav_output/");
                       // window.alert("startTxt="+startTxt);
			var endTxt = resTxt.indexOf(".mp3",startTxt);
			var spCode = resTxt.substring(startTxt,endTxt);
                           //window.alert("startTxt="+startTxt+"endTxt="+endTxt+"spCode="+spCode);
		/*	if(startTxt!=-1 && endTxt!=-1){
				document.getElementById("t2vPlayer").childNodes[1].data = "http://vozme.com/dewplayer-multi.swf?mp3=http://www.text2speech.org/"+spCode+".mp3&autoplay=1";
				document.getElementById("t2vDownloadLink").href = "http://www.text2speech.org/"+spCode+".mp3";
				document.getElementById("t2vDownloadLink").innerHTML = "Download mp3";
			}*/
/*
if(startTxt!=-1 && endTxt!=-1){
				document.getElementById("t2vPlayer").childNodes[1].data = "http://vozme.com/dewplayer-multi.swf?mp3=http://tts.cdacmumbai.in/"+spCode+".mp3&autoplay=1";
				document.getElementById("t2vDownloadLink").href = "http://tts.cdacmumbai.in/"+spCode+".mp3";
				document.getElementById("t2vDownloadLink").innerHTML = "Download mp3";
			}
*/
/*
 document.getElementById("t2vPlayer").childNodes[1].data = "http://vozme.com/dewplayer-multi.swf?mp3=http://tts.cdacmumbai.in/wav_output/fest_out"+count+".mp3&autoplay=1";
document.getElementById("t2vPlayer").childNodes[1].data = "http://tts.cdacmumbai.in/dewplayer.swf?mp3=http://tts.cdacmumbai.in/wav_output/fest_out"+count+".mp3&autoplay=1";
*/



document.getElementById("t2vPlayer").childNodes[1].data = "http://tts.cdacmumbai.in/dewplayer.swf?mp3=http://tts.cdacmumbai.in/wav_output/fest_out"+count+".mp3&autoplay=1";



				document.getElementById("t2vDownloadLink").href = "http://tts.cdacmumbai.in/wav_output/fest_out"+count+".mp3";
				

document.getElementById("t2vDownloadLink").innerHTML = "Download mp3";


                        //  document.getElementById("t2vPlayer").childNodes[1].data = "http://vozme.com/dewplayer-multi.swf?mp3=http://tts.cdacmumbai.in/wav_output/fest_out.mp3&autoplay=1";
			//	document.getElementById("t2vDownloadLink").href = "http://tts.cdacmumbai.in/wav_output/fest_out.mp3";
			//	document.getElementById("t2vDownloadLink").innerHTML = "Download mp3";




  			document.getElementById("t2vSpeak").childNodes[0].src = "chrome://text2voice/content/images/t2v-loader.jpg";
  		}
  	}
  	http.send(params);
 }