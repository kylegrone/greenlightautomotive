function SnapShot(){
	this.cancel_button = null;
	this.snap_button = null;
	this.image_div = null;
	this.auto_flash_on_button  = null;
	this.auto_flash_off_button  = null;
	this.snap_enable_button = null;
	this.snap_process_url = null;
	this.video = null;
	this.cancel_button = $("#snap_cancel")
	this.video_id = "video";
	this.videoObj = { "video": true }
	this.crop_selector_id ="snap_selector" 
//	this.crop_selector = $(this.crop_selector_selector);
	var self =this
	this.canvas = "#snap_container";
	this.context = null;
	this.canvas_2 = "#snap_container_2";
	this.canvas_name = "snap_container";
	this.image_control_sf = "snap_image_sf";
	this.canvas_2_name = "snap_container_2";
	this.loading_container = $("#loading_page");
	this.video_source_id = "video_source";
	this.video_source_label_id = "video_source_label";
	this.video_main_id = "camera_main_container";
	this.crop_image_btn = "crop_image_btn";
	this.canvas_and_button_container = "canvas_and_button_container";
//	this.video_main_container = $(this.video_main_selector);
	
	this.context2 = null;
	this.clip_y= 200 ;
	this.ocr_observers = []
	this.cropped_data = null
	this.videoPlayer = null;
	self.crop_image_modal_id = "crop_image_modal"
//	this.is_safari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
	this.is_safari = /iPad|iPhone|iPod/i.test(navigator.userAgent) && !window.MSStream;
//	this.is_safari = true;
	this.vin_image_data_control = $("#vin_data")
	this.vin_image_preview = $("#vin_image_preview")
	this.addHtml = function(){
		this.crop_modal = '<div class="modal crop_image_modal fade" tabindex="-1" role="dialog" id="'+self.crop_image_modal_id+'"  >'+
		  '<div class="modal-dialog">'+
		    '<div class="modal-content">'+
		      '<div class="modal-header">'+
		        '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
		      			'<span aria-hidden="true">&times;</span></button>'+
		        '<h4 class="modal-title">Crop Image</h4>'+
		      '</div>'+
		      '<div class="modal-body">'+
		        '<h4 class="modal_desc"></h4>'+
		        		
		        		'<canvas id="'+self.canvas_name+'"  height="335" ></canvas>'+
		        		'<canvas id="'+self.canvas_2_name+'" height="100" style="display:none;"></canvas>'+ 		
		       '</div>'+
		      '<div class="modal-footer">'+
		       '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'+
	    		'<button type="button" class="btn btn-primary crop_image_btn" id="'+self.crop_image_btn+'" data-service_id="">Process</button>'+
		      			
		      			
		      '</div>'+
		     
		    '</div><!-- /.modal-content -->'+
		  '</div><!-- /.modal-dialog -->'+
		'</div><!-- /.modal -->';
		$("body").append(self.crop_modal);
		$("#"+self.video_main_id).append('<video id="'+self.video_id+'"   autoplay width="100%" height="335"></video>');
		$("#"+self.video_main_id).append('<div id="'+self.crop_selector_id+'"  style="	border:dotted 3px black;width:100%;height:150px;display:none;top:100px; "></div>');
	}
	this.initiate = function(){
		self.vin_image_data_control.hide();
		this.addHtml();
		if(self.is_safari == false){
				if (typeof MediaStreamTrack === 'undefined' ||
					    typeof MediaStreamTrack.getSources === 'undefined') {
						$("#"+self.video_source_label_id).hide();
						$("#"+self.video_source_id).hide();
		
					} else {
					  MediaStreamTrack.getSources(self.gotSources);
					}
		}else{
			
			
			self.vin_image_preview.detach().prependTo("#"+self.video_main_id);
			$("#"+self.video_id).hide();
			
			$("#"+self.video_source_label_id).hide();
			$("#"+self.video_source_id).hide();
			$("#"+self.canvas_and_button_container).hide()
		}
		self.disableAllButtons();
		self.attachEventListeners();
		
	}
	
	this.gotSources = function (sourceInfos) {
		
		  for (var i = 0; i !== sourceInfos.length; ++i) {
		    var sourceInfo = sourceInfos[i];
		    var option = document.createElement('option');
		    option.value = sourceInfo.id;
		    if (sourceInfo.kind === 'audio') {

		    } else if (sourceInfo.kind === 'video') {
		    	$("#"+self.video_source_id).html("<option value=''>"+ sourceInfo.label || 'camera ' + ( $("#"+self.video_source_id).length + 1)+"</option>")
		    } else {
		      console.log('Some other kind of source: ', sourceInfo);
		    }
		  }
		}
	
	
	this.callObservers = function(text){
		$(self.ocr_observers).each(function(k,v){
			v(text)//calling the observers
			
		})
	}
	
	this.attachObservers =function(fn){
		self.ocr_observers.push(fn);
	}
	this.disableAllButtons=function(){
		self.auto_flash_on_button.prop("disabled","disabled");
		self.auto_flash_off_button.prop("disabled","disabled");
		self.snap_button.prop("disabled","disabled");
		self.cancel_button.prop("disabled","disabled");
		if(self.context !=null){
//			self.context.clearRect(0,0,$("#"+self.video_id).width(),$("#"+self.video_id).height());
		}
	}
	
	this.enableAllButtons = function (){
		self.auto_flash_on_button.removeProp("disabled");
		self.auto_flash_off_button.removeProp("disabled");
		self.snap_button.removeProp("disabled");
		self.cancel_button.removeProp("disabled");
	}
	
	this.flashOnOffButton = function(){
			if(self.auto_flash_on_button.hasClass("btn-success")){
				self.auto_flash_on_button.removeClass("btn-success");
				self.auto_flash_off_button.addClass("btn-danger");
				self.auto_flash_on_button.html("&nbsp;");
				self.auto_flash_off_button.html("OFF");
			}else{
				self.auto_flash_on_button.addClass("btn-success");
				self.auto_flash_off_button.removeClass("btn-danger");
				self.auto_flash_on_button.html("ON");
				self.auto_flash_off_button.html("&nbsp;");
			}
	}
	
	
	this.setCanvas = function(){
		
		$(self.canvas).prop("width",$("#"+self.video_id).width());
		$(self.canvas_2).prop("width",$("#"+self.video_id).width());
		$("#"+self.crop_selector_id).prop("width",$("#"+self.video_id).width());
				
	}
	
	this.enableCamera = function(){
		console.info("enabling camera")
		if(self.is_safari==false){
		//		self.setCanvas();
				self.videoPlayer = $("#"+self.video_id)[0]
				var videoObj  = self.videoObj
				var videoSource = $("#"+self.video_source_id).val();//videoSelect.value;
				
				var constraints = {
						   
						    video: {
						      optional: [{
						        sourceId: videoSource
						      }]
						    }
				};
				if(navigator.getUserMedia) { // Standard
					navigator.getUserMedia(constraints, self.loadStream,self.cameErr);
		
				} else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
		//			navigator.webkitGetUserMedia(constraints, self.loadStream,self.cameErr);
					navigator.webkitGetUserMedia(videoObj, function(stream){
						self.videoPlayer.src = window.webkitURL.createObjectURL(stream);
						self.videoPlayer.play();
						
					}, self.cameErr);
					self.enableCropper();
				}
				else if(navigator.mozGetUserMedia) { // Firefox-prefixed
					navigator.mozGetUserMedia(constraints, self.loadStream,self.cameErr);
					navigator.mozGetUserMedia(videoObj, function(stream){
						self.videoPlayer.src = window.URL.createObjectURL(stream);
						self.videoPlayer.play();
						
					}, self.cameErr);
					self.enableCropper();
				}
		}else{
			
			$("#"+self.image_control_sf).trigger('click');
		}
		
	}

	this.loadFromFile = function(file){
		alert("from file")
	}
	this.loadStream = function(stream){
		  window.stream = stream; // make stream available to console
		  self.videoPlayer.src = window.URL.createObjectURL(stream);
		  self.videoPlayer.play();
	}

	this.takePicture = function(){
		self.setCanvas()
		console.info(self.canvas)
		var video = $("#"+self.video_id)[0];
		var sourceX = 0;
	    var sourceY = self.clip_y;
		self.context = $(self.canvas)[0].getContext("2d");

		self.context.drawImage(video,0,0,$("#"+self.video_id).width(),$("#"+self.video_id).height());
		$("#"+self.crop_image_modal_id).modal('show');
		
		$(self.canvas).cropper({
			minContainerWidth: $("#"+self.video_id).width(),
			maxContainerWidth: $("#"+self.video_id).width(),
			minContainerHeight: $("#"+self.video_id).height(),
			maxContainerHeight: $("#"+self.video_id).height(),
			 crop: function(e) {
			  },
			  built: function (e) {
		          // Strict mode: set crop box data first
		          var container = $(this).cropper('getContainerData');
		          var data = $(self.canvas).cropper("getCanvasData");
		          $(this).cropper('setCropBoxData', {
		            width: data.width,
		            height: $("#"+self.crop_selector_id).height(),
		            left: data.left,
		            top:self.clip_y
		          });
		          
		          
		        }
			});
		
		
		$("body").on("click","#crop_image_btn",function(){
				var canvas_data = $(self.canvas).cropper("getCroppedCanvas");
				console.info(canvas_data);
				self.getImageOCR(canvas_data)
				$("#"+self.crop_image_modal_id).modal('hide');
				$(self.canvas).cropper("destroy")
		});
		$("#"+self.crop_image_modal_id).on('hide.bs.modal', function(e) {
			$(self.canvas).cropper("destroy")
		});
		
	}
	
	this.enableCropper=function(){
		$("#"+self.crop_selector_id).show();
		
	}
	this.disableCropper = function(){
		$("#"+self.crop_selector_id).hide();
	}
	
	this.cameErr = function(error) {
		console.log("Video capture error: ", error.code); 
	}
	
	
	this.disableCamera = function(){
		if(self.is_safari==false){
			self.videoPlayer.pause()
			self.videoPlayer.src=""
		}
	}
	
	this.attachEventListeners = function(){
		
		self.snap_enable_button.click(function(){
			if(self.snap_enable_button.data("enabled")==true && self.is_safari==false){
			
				self.snap_enable_button.css("opacity","1");
				self.disableAllButtons();
				self.snap_enable_button.data("enabled",false);
				self.disableCamera()
			}else{
				
				self.snap_enable_button.data("enabled",true);
				self.enableAllButtons();
				self.enableCamera();
				if(self.is_safari==false){
					self.snap_enable_button.css("opacity","0.5");
				}
			}
			
		});
		self.cancel_button.click(function(){
			self.snap_enable_button.trigger("click");
		})
		self.snap_button.click(function(){
			self.takePicture();
//			self.getImageOCR();
		});
		self.auto_flash_on_button.click(function(){
			self.flashOnOffButton();
			
		});
		self.auto_flash_off_button.click(function(){
			self.flashOnOffButton();
			
		})
		
		$("#"+self.image_control_sf).change(function(evt){
			 var files = evt.target.files;
			    var file = files[0];
			    var validFileType = ".jpg , .png , .bmp";
			    
			    if (files && file) {
			    	var extension = file.name.substring(file.name.lastIndexOf('.'));
			    	if (validFileType.toLowerCase().indexOf(extension) < 0) {
			    		 BootstrapDialog.show({
					            title: 'Error',
					            message: 'Please select a valid file type'
					        });
			    		return 
			    	}
			        var reader = new FileReader();
			        reader.onload = function(readerEvt) {
			           self.getImageOCR( null,readerEvt.target.result)
			        };
			        reader.readAsDataURL(file);
			    }
			
		});
		
	}
	
	self.clearFileInput = function (ctrl) {
		  try {
		    ctrl.value = null;
		  } catch(ex) { }
		  if (ctrl.value) {
		    ctrl.parentNode.replaceChild(ctrl.cloneNode(true), ctrl);
		  }
		}
	this.getImageOCR=function(data,dataUrl){
		var utility = new Utility();
		if(typeof dataUrl =="undefined"){
			var dataUrl  = data.toDataURL();
		}
		self.vin_image_data_control.val(dataUrl);
		self.vin_image_preview.attr("src",dataUrl);
		self.vin_image_preview.show();
//		this.vin_image_preview = $("#vin_image_preview")
		self.loading_container.show();
		var csrftoken = utility.getCookie('csrftoken');//these methods are available in utlitiy
		$.ajax({
			  type: "POST",
			  beforeSend: function(xhr, settings) {
			        if (!utility.csrfSafeMethod(settings.type) && !this.crossDomain) {
			            xhr.setRequestHeader("X-CSRFToken", csrftoken);
			        }
			    },		
			  url: self.snap_process_url,
			  data: { 
			     imgBase64: dataUrl
			  }
			,success:function(data){
				console.info(data)
				self.loading_container.hide();
				if (data["resp"]!="" && data["resp"]!=null){
					self.callObservers(data["resp"]);
				}else{
//					 BootstrapDialog.show({
//				            title: 'Error',
//				            message: 'Unable to process the vin'
//				        });
				}
				self.loading_container.hide();
			},error:function(){
//		        BootstrapDialog.show({
//		            title: 'Error',
//		            message: 'Unable to process the vin'
//		        });
		        self.loading_container.hide();
			}
			}).done(function(o) {
			  console.log('saved'); 
			  self.loading_container.hide()
			  // If you want the file to be visible in the browser 
			  // - please modify the callback in javascript. All you
			  // need is to return the url to the file, you just saved 
			  // and than put the image in your browser.
			});
	}

}
