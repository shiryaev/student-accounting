var x, y
var ie_test = document.all?true:false
var tooltip = document.createElement("div")
function getMouseXY(e) {
	if (ie_test) {
		x = event.clientX + document.body.scrollLeft
		y = event.clientY + document.body.scrollTop
	}
	else {
		x = e.pageX
		y = e.pageY
	}  
	x-=15; y-=25;
	tooltip.style.left = x + "px"
	tooltip.style.top = y + "px"
	return true
}

function tooltip_add(message){
    if (typeof document.onmousemove != 'function') {
            document.onmousemove = getMouseXY;
    }
	document.body.appendChild(tooltip)
	//tooltip.style.left = x-15 + "px"
	//tooltip.style.top = y-25 + "px"

	tooltip.id = "tooltip"
	tooltip.innerHTML = message

}

function tooltip_rm() {
	document.body.removeChild(document.getElementById("tooltip"))
}

function setVal(id,val) {
	document.getElementById(id).value = val;
}

function PreloadImages()
{
 if (document.images)
 {
  var imgFiles = PreloadImages.arguments;
  var preloadArray = new Array();
  for (var i=0; i<imgFiles.length; i++)
  {
   preloadArray[i] = new Image;
   preloadArray[i].src = imgFiles[i];
  }
  }
}

function addLoadEvent(func) {
        var oldonload = window.onload;
        if (typeof window.onload != 'function') {
                window.onload = func;
        }
        else {
                window.onload = function() {
                        oldonload();
                        if (typeof window.onload != 'function') func();
                }
        }
}

function toggleDiv(element){
      if(document.getElementById(element).style.display = 'none')
      {
        document.getElementById(element).style.display = 'block';
      }
      else if(document.getElementById(element).style.display = 'block')
      {
        document.getElementById(element).style.display = 'none';
      }
}
