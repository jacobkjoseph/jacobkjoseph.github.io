/************************************************************************************************/
/*	Programmer: Vishal Rangnath Maral, CDAC Mumbai <vishalrmaral@gmail.com>	, Mani Shankar Bandaru CDAC Mumbai <manishankar417@gmail.com>		*/
/*	Last modified: 16 March 2015.								*/
/************************************************************************************************/

var seltext = null;
var selText = null;
var snd=document.getElementById('noise');
var count = null;
var trackPos;


function playsound(){
	var snd=document.getElementById('noise');
	//alert("from play");
	//snd.src="Kalimba.mp3";
	//snd.src="http://tts.cdacmumbai.in/wav_output/fest_out"+count+".wav";
	snd.src="http://tdil-dc.in/tts/wav_output/fest_out"+count+".mp3";
    	snd.load();
    	snd.play();
	snd.addEventListener('ended', stopAnimation);
}
function pausesound(){
    	var snd=document.getElementById('noise');
    	snd.pause();
	snd.addEventListener('ended', stopAnimation);//added for modification

	var popup=chrome.extension.getViews({type:'popup'})[0];
	var loaderImage = popup.document.getElementById("loaderImage");

	loaderImage.style.visibility="visible";
	loaderImage.src="images/emblam.png";
}

function replaysound(){
	//alert("from Replay");
	var snd=document.getElementById('noise');
	snd.currentTime=0;
	snd.play();
}

function stopAnimation()
{
	//alert('Hola');
	var popup=chrome.extension.getViews({type:'popup'})[0];
	var loaderImage = popup.document.getElementById("loaderImage");

	//loaderImage.style.visibility="hidden";
	loaderImage.src="images/emblam.png";
}

function animate()
{
	var popup=chrome.extension.getViews({type:'popup'})[0];
	if(popup)
	{
		//	alert(" popup captured");
		var loaderImage = popup.document.getElementById("loaderImage");
		//if(loaderImage)
		//	alert("loader image captured");
		loaderImage.src="images/playing1.gif";
		localStorage["loaderImage"]="playing1.gif";
	}
}

function send_req()
{
	var language = localStorage["favorite_language"] || "hindi";
	var voiceSpeed=localStorage["speed"];
	//alert("language from local storage is--"+language);
	if(lang==language && voiceSpeed==speed && selText==seltext)//version 1.0 condition-->(selText==seltext)
	{
		animate();
		//playsound();		
		var snd=document.getElementById('noise');
	    	snd.play();
		//snd.addEventListener('ended', stopAnimation);
	}
	else
	{
		//alert("sending request");
		selText=seltext;
		//alert("seltext-->"+seltext);
		//alert("select has text");
		var vc = "voice1";
		var lang=localStorage["favorite_language"] || "hindi";
		var speed=localStorage["speed"];
		//var lang="marathi";
		//var url = "http://tts.cdacmumbai.in/festival_cs_plugin.php";
		var url = "http://tdil-dc.in/tts/festival_cs_plugin.php";
	    	count =  Math.floor( Math.random()*100000000 +1 );
	    	//window.alert("count="+count);
	      	var params = "Languages="+lang+"&voice="+vc+"&ex=execute&op="+selText+"&count="+count+"&speed="+speed;  
	    //window.alert(params);     
	  	http = new XMLHttpRequest();
	  	http.open("POST", url, true);
	  	//Send the proper header information along with the request
	  	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	  	http.setRequestHeader("Content-length", params.length);
	  	http.setRequestHeader("Connection", "close");
	  	http.onreadystatechange = function() {
			if(http.readyState == 4) {
				var resTxt = http.responseText;
				animate();
				playsound();
	  		}
		  	}
	  	http.send(params);
			//alert("request sent from background");
	}
 }

function placeCall()
{
	if(seltext && seltext!="" && seltext!=" ")
		//alert("click received for "+request.directive+" "+seltext);
		send_req();				
	else
	{
		stopAnimation();
		alert("Please select text to speak");//do NOT comment this
		break;
	}
}

	
chrome.extension.onMessage.addListener(
    function(request, sender, sendResponse) 
	{
	//alert("from background.js");
        switch (request.directive) {
        	case "play":
			
			if(seltext && seltext!="" && seltext!=" ")
				//alert("click received for "+request.directive+" "+seltext);
				send_req();				
			else
			{
				stopAnimation();
				alert("Please select text to speak");//do NOT comment this
				break;
			}
					//playsound();
            		break;
		case "pause":
			//alert("click received for "+request.directive);
            		pausesound();
            		break;
		case "replay":
			//alert("click received for "+request.directive);
            		replaysound();
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

function rightClick()
{	
	//alert("hi Vishal");
	chrome.contextMenus.removeAll();
	chrome.contextMenus.create({ "title" : "Speakit!","type" : "normal","contexts" : ["selection"], //the context which item appear
	  "onclick" : speakOnClick // The function call on click
	});
}
function speakOnClick(info, tab) 
{
	
	seltext = info.selectionText;
	//alert(seltext);
	//window.open("popup.html", "window", "width=300,height=300,status=yes,scrollbars=yes,resizable=yes");
	
	send_req();		

	/*if(seltext && seltext!="" && seltext!=" ")
		//alert("click received for "+request.directive+" "+seltext);
		send_req();				
	else
	{
		stopAnimation();
		alert("Please select text to speak");//do NOT comment this
		break;
	}*/
				
}

rightClick();

