function getFactors(num) {
  const isEven = num % 2 === 0;
  let inc = isEven ? 1 : 2;
  let factors = [1, num];

  for (let curFactor = isEven ? 2 : 3; Math.pow(curFactor, 2) <= num; curFactor += inc) {
    if (num % curFactor !== 0) continue;
    factors.push(curFactor);
    let compliment = num / curFactor;
    if (compliment !== curFactor) factors.push(compliment);
  }

  return factors.sort(function(a, b){return a-b});
}


function indexOfNearestLessThan(array, needle) {
	if (array.length === 0) return -1;

	var high = array.length - 1,
		low = 0,
		mid,
		item,
		target = -1;
	
	if (array[high] < needle) {
		return high;
	}

	while (low <= high) {
		mid = (low + high) >> 1;
		item = array[mid];
		if (item > needle) {
			high = mid - 1;
		} else if (item < needle) {
			target = mid;
			low = mid + 1;
		} else {
			return low;
		}
	}

	return target;
}

var dieWidth = 500;
var dieHeight = 400;
var streetWidth = 0;
var waferWidth = 0;
var waferHeight = 0;
var aspectRatio = 0;
var smallDieWidth = 0;
var smallDieHeight = 0;
var careAreas = [];
var exclusionZones = [];


document.getElementById('diewidth').onchange = function(e){
     
    calculateWafer();
   changeSwathWidth();
}


document.getElementById('dieheight').onchange = function(e){
    
    calculateWafer();
   changeSwathHeight();
}

document.getElementById('dierows').onchange = function(e){
    
    calculateWafer();
   changeSwathWidth();
     changeSwathHeight();
}

document.getElementById('diecolumns').onchange = function(e){
    
    calculateWafer();
   changeSwathWidth();
     changeSwathHeight();
}

document.getElementById('streetwidth').onchange = function(e){
    
    calculateWafer();
   changeSwathWidth();
     changeSwathHeight();
}


function calculateWafer(){
    
     dieWidth = parseInt($("#diewidth")[0].value); 
     dieHeight = parseInt($("#dieheight")[0].value);
     dieRows = parseInt($("#dierows")[0].value);
     dieCols = parseInt($("#diecolumns")[0].value);
     streetWidth = parseInt($("#streetwidth")[0].value);
        waferWidth = (((dieCols + 1) * streetWidth) + (dieCols * dieWidth))
        waferHeight = (((dieRows + 1) * streetWidth) + (dieRows * dieHeight))
        aspectRatio = dieWidth / dieHeight;
        if(dieWidth > dieHeight){
           var  array = getFactors(dieWidth);
         smallDieWidth= array[indexOfNearestLessThan(array, 600)];
        smallDieHeight =smallDieWidth/aspectRatio;
        
        } else {
           var  array = getFactors(dieHeight);
        smallDieHeight= array[indexOfNearestLessThan(array, 600)];
        smallDieWidth = aspectRatio * smallDieHeight;
        
        }
       
       console.log(smallDieWidth);
       console.log(smallDieHeight);
       console.log(aspectRatio);
        var canvas = document.getElementById('canvas');
        canvas.width = smallDieWidth;
        canvas.height = smallDieHeight;
        var ctx = canvas.getContext('2d');
        ctx.beginPath();
        var width = canvas.width;
        var height =canvas.height
        ctx.rect(0,0,width,height);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 1;
        ctx.stroke();
        careAreas = [];
        exclusionZones = [];
        appendCareAndExclusionZones();
        $("#widthinfo").html(waferWidth);
        $("#heightinfo").html(waferHeight);
 
}

function changeSwathWidth(){

     var factors = getFactors(waferWidth);

      var ul = document.getElementById("swathwidth"); // moved this out of the loop for a bit of performance improvement (not relevant to the solution.)
        ul.innerHTML = "";
         var li = document.createElement("option");
          li.setAttribute("value", "");
          var linkText = document.createTextNode("Choose...");
            li.appendChild(linkText);
          ul.appendChild(li);
      $.each(factors, function(i, v) {
          

          var li = document.createElement("option");
          var linkText = document.createTextNode(v);
            li.appendChild(linkText);
          ul.appendChild(li);
      })

}


function changeSwathHeight(){

     var factors = getFactors(waferHeight);

      var ul = document.getElementById("swathheight"); // moved this out of the loop for a bit of performance improvement (not relevant to the solution.)
      ul.innerHTML = "";
               var li = document.createElement("option");
               li.setAttribute("value", "");
          var linkText = document.createTextNode("Choose...");
            li.appendChild(linkText);
          ul.appendChild(li);
      $.each(factors, function(i, v) {
      
       
          var li = document.createElement("option");
          var linkText = document.createTextNode(v);
            li.appendChild(linkText);
          ul.appendChild(li);
      })

}


function appendCareAndExclusionZones(){

     var factors = getFactors(waferHeight);

      var ul = document.getElementById("careEntries"); // moved this out of the loop for a bit of performance improvement (not relevant to the solution.)
      ul.innerHTML = "";
      $.each(careAreas, function(i, v) {
     
          var li = document.createElement("li");
          li.className = "list-group-item list-group-item-success";
          var linkText = document.createTextNode("Top Left : x - "+v["top_left"].x +", y - "+ v["top_left"].y +" || Bottom Right : x - "+v["bottom_right"].x + ", y - "+v["bottom_right"].y );
            li.appendChild(linkText);
          ul.appendChild(li);
      })
      
      
      var ul = document.getElementById("exeEntries"); // moved this out of the loop for a bit of performance improvement (not relevant to the solution.)
      ul.innerHTML = "";
      $.each(exclusionZones, function(i, v) {
     
          var li = document.createElement("li");
          li.className = "list-group-item list-group-item-danger";
          var linkText = document.createTextNode("Top Left : x - "+v["top_left"].x +", y - "+ v["top_left"].y +" || Bottom Right : x - "+v["bottom_right"].x + ", y - "+v["bottom_right"].y );
            li.appendChild(linkText);
          ul.appendChild(li);
      })

}


function generate(){

 var forms = document.querySelectorAll('form')
 Array.prototype.slice.call(forms)
    .forEach(function (form) {
     
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()

        } else {
          var generate = {};
          var die = {};
          die.width = parseInt($("#diewidth")[0].value); 
          die.height =  parseInt($("#dieheight")[0].value);
          die.rows = parseInt($("#dierows")[0].value);
          die.columns =   parseInt($("#diecolumns")[0].value);
          generate.die = die;
          generate.pattern = $("#pattern")[0].value
          var patternAttr = {}
          patternAttr.scaling = 30
          patternAttr.patternbgr =   $("#patternbgr")[0].value
          generate["pattern_attr"] = patternAttr; 
          generate["street_width"] = parseInt($("#streetwidth")[0].value);
          generate.swath = {}
          generate.swath.width =  parseInt($("#swathwidth")[0].value); 
          generate.swath.height =   parseInt($("#swathheight")[0].value); 
          generate.user_id =  $("#userid")[0].value; 
          generate["impurities_per_die"] =parseInt($("#impurities")[0].value); 
          console.log(generate);
          generate["care_areas"] = careAreas
          generate["exclusion_zones"] = exclusionZones
          generate["impurity_luminance"] = $("#impurityluminance")[0].value; 
          
              
          $.ajax({
              url:"/data/generate",
              type:"POST",
              data:JSON.stringify(generate),
              contentType:"application/json; charset=utf-8",
              dataType:"json",
              success: function(){
           
              }
        })
          
          
        }

        form.classList.add('was-validated')
     
    })


}



var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
//Variables
var canvasx = $(canvas).offset().left;
var canvasy = $(canvas).offset().top;
var last_mousex = last_mousey = 0;
var last_mousexwrb = last_mouseywrb = 0;
var mousex = mousey = 0;
var mousexwrb = mouseywrb = 0;
var mousedown = false;

window.onload = function(){
    calculateWafer();
    changeSwathWidth();
    changeSwathHeight();
    
    
    ctx.beginPath();
    var width = canvas.width;
    var height =canvas.height
    ctx.rect(0,0,width,height);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 1;
    ctx.stroke();
}



//Mousedown
$(canvas).on('mousedown', function(e) {
 var rect = canvas.getBoundingClientRect();
   
    last_mousex = parseInt(e.clientX-Math.round(rect.left));
	last_mousey = parseInt(e.clientY-Math.round(rect.top));
	last_mousexwrb = parseInt(e.clientX-Math.round(rect.left));
	last_mouseywrb = canvas.height - parseInt(e.clientY-Math.round(rect.top));
    mousedown = true;
});
$(canvas).on("contextmenu",function(e){
       return false;
    });
//Mouseup
$(canvas).on('mouseup', function(e) {
   

     var rect = canvas.getBoundingClientRect();
   
    mousex = parseInt(e.clientX-Math.round(rect.left));
	mousey = parseInt(e.clientY-Math.round(rect.top));
	
	          
    if(mousedown) {
    //    ctx.clearRect(0,0,canvas.width,canvas.height); //clear canvas
        var width = mousex-last_mousex;
        var height = mousey-last_mousey;
    
        var xtlwrb = last_mousex;
        var ytl = 0;
        var ytlwrb = 0;
        
        var xbrwrb = mousex;
        var ybr = 0;
        var ybrwrb = 0;
        if(height < 0){
        
            ytl = mousey;
            ytlwrb = canvas.height - ytl;
            
            ybr = last_mousey ;
            ybrwrb = canvas.height - ybr;  
             
        } else {
        
            ytl = last_mousey;
            ytlwrb = canvas.height - ytl;
            
            ybr = mousey;
            ybrwrb = canvas.height - ybr;   
        }
       
        
        
        var dieWidth = parseInt($("#diewidth")[0].value); 
        var dieHeight = parseInt($("#dieheight")[0].value);
    
       if (event.button == 0) {
       
            ctx.beginPath();

            ctx.rect(last_mousex,last_mousey,width,height);
            ctx.strokeStyle = 'green';
            ctx.lineWidth = 1;
            ctx.stroke();


            var careArea = {};
            careArea["top_left"] = {};
            careArea["top_left"].x = Math.ceil((xtlwrb / canvas.width) * dieWidth); 
            careArea["top_left"].y = Math.ceil((ytlwrb / canvas.height) * dieHeight);
            
            careArea["bottom_right"] = {};
            careArea["bottom_right"].x  = Math.ceil((xbrwrb / canvas.width) * dieWidth); 
            careArea["bottom_right"].y =  Math.ceil((ybrwrb / canvas.height) * dieHeight);
  
            careAreas.push(careArea);
            
        }
        
        
         if (event.button == 2){
         
            ctx.beginPath();
            var width = mousex-last_mousex;
            var height = mousey-last_mousey;
            ctx.rect(last_mousex,last_mousey,width,height);
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 1;
            ctx.stroke();


            var exclusionZone = {};
            exclusionZone["top_left"] = {};
            exclusionZone["top_left"].x =  Math.ceil((xtlwrb / canvas.width) * dieWidth); 
            exclusionZone["top_left"].y = Math.ceil((ytlwrb / canvas.height) * dieHeight);
            
            exclusionZone["bottom_right"] = {};
            exclusionZone["bottom_right"].x  = Math.ceil((xbrwrb / canvas.width) * dieWidth); 
            exclusionZone["bottom_right"].y = Math.ceil((ybrwrb / canvas.height) * dieHeight);
  
            exclusionZones.push(exclusionZone);
            event.stopPropagation()
        }
        
        appendCareAndExclusionZones();
    }
    
    
     mousedown = false;
     
    
});

//Mousemove
$(canvas).on('mousemove', function(e) {
  
     var rect = canvas.getBoundingClientRect();
     mousexwrb = parseInt(e.clientX-Math.round(rect.left));
	 mouseywrb = canvas.height - parseInt(e.clientY-Math.round(rect.top));

    $('#output').html('Current Pos: '+mousexwrb+', '+mouseywrb+'<br/>Last Pos: '+last_mousexwrb+', '+last_mouseywrb+'<br/>Drawing: '+mousedown);
});

