// Save this script as `options.js`

// Saves options to localStorage.
function save_options() {
 // language="hindi";
  languageset = document.getElementsByName("language");
  for (var i = 0; i < languageset.length; i++)
	{
		if(languageset[i].checked)
		{
			var language=languageset[i].value;
			break;
		}
	}
  localStorage["favorite_language"] = language;
	//speed="normal"
	var speedset = document.getElementsByName("speed");
  for (var i = 0; i < languageset.length; i++)
	{
		if(speedset[i].checked)
		{
			var speed=speedset[i].value;
			break;
		}
	}
	
	localStorage["speed"] = speed;
  // Update status to let user know options were saved.
  var status = document.getElementById("status");
  status.innerHTML = language+" "+speed+" Options Saved.";
  setTimeout(function() {
    status.innerHTML = "";
  }, 1000);
}

// Restores select box state to saved value from localStorage.
function restore_options() {
  var favorite = localStorage["favorite_language"];
  if (!favorite) {
    return;
  }
  var languageset = document.getElementByName("language");
  for (var i = 0; i < languageset.length; i++)
  {
    var langradio = languageset[i];
    if (langradio.value == favorite) {
      languageset[i].checked = "true";
      break;
    }
  }
  
  var stored_speed = localStorage["speed"];
  if (!stored_speed) {
    return;
  }
  var speedset = document.getElementByName("speed");
  for (var i = 0; i < speedset.length; i++)
  {
    var speedradio = speedset[i];
    if (speedradio.value == stored_speed) {
      speedset[i].checked = "true";
      break;
    }
  }
}
document.addEventListener('DOMContentLoaded', restore_options);
document.querySelector('#save').addEventListener('click', save_options);
