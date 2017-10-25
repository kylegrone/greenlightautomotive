function InspectionCategoriesDiv(div){
	var self = this;
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
	self.statusRadio = $(div).find("input:radio");
	self.colorDiv = $(div); 
	self.cameraButton = $(div).find(".camera");
	self.status = $(div).find("form").find(".status");
	self.imageCanvas = $(div).find("form").find("canvas");
	self.safariCameraButton = $(div).find(".safari_camera");
	self.isSafari  = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
	self.bindEvents = function(){
		self.statusRadio.on("change",function(){
			var value = $(this).val();
			self.status.val(value);
			self.colorDiv.removeClass("alert-success").removeClass("alert-danger").removeClass("alert-warning").addClass(value == "pass" ? "alert-success":(value=="fail" ? "alert-danger" :"alert-warning" ));
			
		});
//		self.safariCameraButton.off("change").on("change",function(evt){
//			var files = evt.target.files;
//		    var file = files[0];
//		    var canvas = self.imageCanvas[0];
//		    if (files && file) {
//		        var reader = new FileReader();
//
//		        reader.onload = function(readerEvt) {
//		            var img = new Image();
//		            img.onload = function(){
//		                 canvas.width=img.width
//		                 canvas.height=img.height;
//		            	canvas.getContext("2d").drawImage(img,0,0,img.width,img.height);
//		            	$(self.imageCanvas).attr("data-image","true");
//		            	
//		            }
//		            img.src = readerEvt.target.result;
//		        };
//		        reader.readAsDataURL(file);
//		    }
//		});
		self.safariCameraButton.off("change").on("change",function(e){
	            e.preventDefault();
	            var canvas = self.imageCanvas[0];
	            if(this.files.length === 0) return;
	            var imageFile = this.files[0];
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
	                    exif=EXIF.readFromBinaryFile(createBinaryFile(d.target.result));
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
	                    var ctx = canvas.getContext("2d");
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
//	                        ctx.setTransform(1, 0, 0, 1, 0, 0);
	                        ctx.drawImage(img, 0, 0, width, height);
	                    }
	                    ctx.setTransform(1, 0, 0, 1, 0, 0);
	                    $(self.imageCanvas).attr("data-image","true");
	                };
	                binaryReader.readAsArrayBuffer(imageFile);
	                
	            };
	        });
		self.cameraButton.off("click").on("click",function(){
			if(!self.isSafari){
			var modal = new CameraModal(self.imageCanvas);
			 modal.init();
			}
			else{
				self.safariCameraButton.trigger("click");
			} 
		});
		
	}
	
}