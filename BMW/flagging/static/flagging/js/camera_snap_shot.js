function CameraSnapShot(){
	var self = this;
	self.video = null;
	self.canvas = null;
	self.videoObj = {"video":true};
	self.tempVideo = null;
	self.setCanvas = function(canvas){
		
		self.canvas = canvas	;
		self.context = self.canvas.getContext("2d");
	}
	self.setVideo = function(video){
		self.video = video;
	}
	self.error = function(error){
		alert(error);
	}
	self.init = function(){
		
		if(navigator.getUserMedia) { // Standard
			navigator.getUserMedia(self.videoObj, function(stream) {
				self.video.src = window.URL.createObjectURL(stream);
				self.video.play().then(function(){
				});
			}, self.error);
		} else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
			navigator.webkitGetUserMedia(self.videoObj, function(stream){
				self.video.src = window.URL.createObjectURL(stream);
				self.video.play().then(function(){
				});
			}, self.error);
		}
		else if(navigator.mozGetUserMedia) { // Firefox-prefixed
			navigator.mozGetUserMedia(self.videoObj, function(stream){
				self.video.src = window.URL.createObjectURL(stream);
				self.video.play().then(function(){
				});
			}, self.error);	
	}	
	}
	self.stop = function(){
		self.video.pause();
	}
	self.capturePicture = function(){
		self.tempVideo = self.video;
		self.context.drawImage(self.tempVideo, 0, 0, 320, 240);
	}
	self.getImage = function(){
		return self.tempVideo;
	}
	
}

