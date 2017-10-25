
(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.
	var createBinaryFile = function(uintArray) {
	    var data = new Uint8Array(uintArray);
	    var file = new BinaryFile(data);
	    file.getByteAt = function(iOffset) {
	        return data[iOffset];
	    };
	    file.getBytesAt = function(iOffset, iLength) {
	        var aBytes = [];
	        for (var i = 0; i < iLength; i++) {
	            aBytes[i] = data[iOffset  + i];
	        }
	        return aBytes;
	    };
	    file.getLength = function() {
	        return data.length;
	    };
	    return file;
	};
  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;
  var localstream = null;
  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  function startup() {
	width = 320;    // We will scale the photo width to this
	height = 0;     // This will be computed based on the input stream
	  // |streaming| indicates whether or not we're currently streaming
	  // video from the camera. Obviously, we start at false.

	streaming = false;
	localstream = null;
	  // The various HTML elements we need to configure or control. These
	  // will be set by the startup() function.

	video = null;
	canvas = null;
	photo = null;
	startbutton = null;
	width = 320
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    navigator.getMedia = ( navigator.getUserMedia ||
                           navigator.webkitGetUserMedia ||
                           navigator.mozGetUserMedia ||
                           navigator.msGetUserMedia);

    navigator.getMedia(
      {
        video: true,
        audio: false
      },
      function(stream) {
        if (navigator.mozGetUserMedia) {
          video.mozSrcObject = stream;
          localstream = stream;
        } else {
          var vendorURL = window.URL || window.webkitURL;
          video.src = vendorURL.createObjectURL(stream);
        }
        video.play();
      },
      function(err) {
        console.log("An error occured! " + err);
      }
    );

    video.addEventListener('canplay', function(ev){
    	
      if (!streaming) {
    	  
        height = video.videoHeight / (video.videoWidth/width);
      
        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);
    
    startbutton.addEventListener('click', function(ev){
      takepicture();
    	ev.preventDefault();
      
    }, false);
    
   // clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }
  
  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

  function takepicture() {
	
    var context = canvas.getContext('2d');
    if (width && height) {
    	
      canvas.width = video.width;
      canvas.height = video.height;
      context.drawImage(video, 0, 0, width, height);
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
      $(".addnotes").trigger("click");
    } else {
      clearphoto();
    }
  }
  
  

  $(document).on('click','#startcamera',function(){
	    $('#imagemap').addClass('hidden');	
	    $('.camera').removeClass('hidden');
	  	$('.canvas').removeClass('hidden');
	  	$('.output').removeClass('hidden');
	  	$('#canclebutton').removeClass('hidden');
		startup();
	});
  $(document).on('click','#canclebutton',function(){
	  $('.camera').addClass('hidden');
	  	$('.canvas').addClass('hidden');
	  	$('.output').addClass('hidden');
	  	$(this).addClass('hidden');
	  	$('#photo').removeAttr('src');
	  	$('#imagemap').removeClass('hidden');
	  	if(localstream){
	  		localstream.pause();
	  	    localstream.src = "";
	  	}
	  	$('#video').load();
  });
  $(document).on('change','#safarifile' , function(e){
	  debugger;
		$('#imagemap').addClass('hidden');
		$('.canvas').removeClass('hidden');
	  	$('.soutput').removeClass('hidden');
		$('#canclesafaricam').removeClass('hidden');
		canvas = document.getElementById('canvas');
		photo = document.getElementById('photo');
		sphoto = document.getElementById('sphoto');
		var context = canvas.getContext('2d');
		var file = e.target.files[0];
		if(e.target.files && file){
//			 var reader = new FileReader();
//			 reader.onload = function(readerEvt) {
//				 var img = new Image();
//				 img.onload = function() {
//					 	canvas.width = img.width;
//					 	canvas.height = img.height;
//				    	context.drawImage(img,0,0, img.width,img.height);
//			        	var data = canvas.toDataURL('image/png');
//			        	photo.setAttribute('src', data);
//			        	sphoto.setAttribute('src', data);
//				    } 
//				 img.src = readerEvt.target.result;
//			 }
//			 reader.readAsDataURL(file);
			var imageFile = file;
            var img = new Image();
            var url = window.URL ? window.URL : window.webkitURL;
            img.src = url.createObjectURL(imageFile);
            img.onload = function(e) {
                url.revokeObjectURL(this.src);
                var width;
                var height;
                var binaryReader = new FileReader();
                binaryReader.onloadend=function(d) {
                    var exif, transform = "none";
                    exif=EXIF.readFromBinaryFile(d.target.result);
                    if(exif.Orientation === 8) {
                        width = img.height;
                        height = img.width;
                        transform = "left";
                    } else if(exif.Orientation === 6) {
                        width = img.height;
                        height = img.width;
                        transform = "right";
                    } else if(exif.Orientation === 1) {
                        width = img.width;
                        height = img.height;
                    } else if(exif.Orientation === 3) {
                        width = img.width;
                        height = img.height;
                        transform = "flip";
                    } else {
                        width = img.width;
                        height = img.height;
                    }
                   
                    width = canvas.width =img.width*0.5;
                    height = canvas.height = img.height*0.5;
                    var ctx = context;
                    ctx.fillStyle = 'white';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    if(transform === 'left') {
                        ctx.setTransform(0, -1, 1, 0, 0, height);
                        ctx.drawImage(img, 0, 0, height, width);
                    } else if(transform === 'right') {
                        ctx.setTransform(0, 1, -1, 0, width, 0);
                        ctx.drawImage(img, 0, 0, height, width);
                    } else if(transform === 'flip') {
                        ctx.setTransform(1, 0, 0, -1, 0, height);
                        ctx.drawImage(img, 0, 0, width, height);
                    } else {
//                        ctx.setTransform(1, 0, 0, 1, 0, 0);
                        ctx.drawImage(img, 0, 0, width, height);
                    }
                    ctx.setTransform(1, 0, 0, 1, 0, 0);
                    var data = canvas.toDataURL('image/png');
		        	photo.setAttribute('src', data);
		        	sphoto.setAttribute('src', data);
		        	$(".addnotes").trigger("click");
                };
                binaryReader.readAsArrayBuffer(imageFile);
                
            };
		}
//		var img = new Image();
//		img.src = URL.createObjectURL(e.target.files[0]);
	      
	});
  	$(document).on('click','#canclesafaricam',function(){
  		$('.canvas').addClass('hidden');
	  	$('.soutput').addClass('hidden');
		$('#canclesafaricam').addClass('hidden');
		$('#photo').removeAttr('src');
		$('#sphoto').removeAttr('src');
  		$('#imagemap').removeClass('hidden');
  	});
})();