
window.onload = function() 
{ 
	//alert("Page is loaded");
	onloadPlay();
    //var bg = chrome.extension.getBackgroundPage();
    //bg.getPageInfo(onPageInfo);
}


function awesome() {
  //alert("from popup.js");
}

function totallyAwesome() {
  //alert("something TOTALLY awesome!");
}

function awesomeTask() {
  awesome();
  totallyAwesome();
}

function hide() {  
//document.getElementById('loaderImage').style.visibility="hidden";   
        } 
function show() {  
document.getElementById('loaderImage').style.visibility="visible";   
        } 

function onloadPlay() {
	//alert("onload");
	document.getElementById('loaderImage').src="images/loading1.gif";
	show();
  	chrome.extension.sendMessage({directive: "play"}, function(response) {
        //this.close(); // close the popup when the background finishes processing request
    });
  
}


function clickHandlerPlay(e) {
	//setTimeout(awesomeTask, 100);
	document.getElementById('loaderImage').src="images/loading1.gif";
	show();
  	chrome.extension.sendMessage({directive: "play"}, function(response) {
        //this.close(); // close the popup when the background finishes processing request
    });
  
}

function clickHandlerReplay(e) {
	//setTimeout(awesomeTask, 100);
	document.getElementById('loaderImage').src="images/playing1.gif";
	show();
  	chrome.extension.sendMessage({directive: "replay"}, function(response) {
        //this.close(); // close the popup when the background finishes processing request
    });
  
}

function clickHandlerPause(e) {
  //setTimeout(awesomeTask, 100);
	hide();
	chrome.extension.sendMessage({directive: "pause"}, function(response) {
        //this.close(); // close the popup when the background finishes processing request
    });
  
}

function reloader() 
{
	var bg=chrome.extension.getBackgroundPage();
	var audio=bg.document.getElementById('noise');
	//alert(audio.readyState);
	
	/*else if(audio.readyState>=0 ||audio.readyState<=3)//audio not completely loaded on background page
	{
		document.getElementById('loaderImage').src="images/loading1.gif";
		show();
	}*/
	if(audio.paused||audio.ended)//audio not completely loaded on background page
	{
		hide();
	}
	else if(audio.readyState>=4)//audio completely loaded on background page
	{
		document.getElementById('loaderImage').src="images/playing1.gif";
		show();
	}
}

// Add event listeners once the DOM has fully loaded by listening for the
// `DOMContentLoaded` event on the document, and adding your listeners to
// specific elements when it triggers.
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('play').addEventListener('click', clickHandlerPlay);
  document.getElementById('pause').addEventListener('click', clickHandlerPause);
  document.getElementById('replay').addEventListener('click', clickHandlerReplay);
	reloader();
});
