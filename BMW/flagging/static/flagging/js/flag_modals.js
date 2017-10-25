function CustomerFacingFlagsModal(flag,roId){
	
	var self = this;
	self.modal = "flaggingModal";
	self.modalBody = "flaggingModalBody";
	self.flagType = $(flag).attr("id").split("_")[0];
	self.flagId = $(flag).attr("id").split("_")[1];
	
	self.roId = roId;
	self.count = 0;
	self.init = function(){
		$("#"+self.modal).modal();
		self.generateHtml();
		self.bindEvents();
		
		
	}
	self.generateHtml = function(){
		ajaxRequest(window.get_flag_notes_url,"GET",function(result){
			
			var html = "<textarea rows='4' col='100' readonly style='margin: 0px 0px 10px; width: 541px; height: 69px;'>"+result+" </textarea></br>" +
					"<textarea rows='4' col='100' placeholder='Add additional Notes' id='note' style='margin: 0px 0px 10px; width: 541px; height: 69px;'></textarea>";
			$("#flaggingModalBody").html(html);
		},{"flagId" : self.flagId});
		
		
	}
	
	
	self.bindEvents = function(){
		$("#submitFlag").off("click");
		$("#submitFlag").on("click",function(){
			
			$("#" + self.modal).modal("hide");
			
			var data = {"notes" : $("#note").val(),"flagType" : self.flagType, "flagId" : self.flagId , "roId" : self.roId};
			
			setTimeout(function(){
			ajaxRequest(window.update_flags_url,"GET",updateFlagResponse,data);
			},300);
			
			
		});
		
	}
	
	
}
function ApprovalNeededModal(flag,roId){
	
	var self = this;
	self.modal = "#flaggingModal";
	self.modalBody = "#flaggingModalBody";
	self.flagType = $(flag).attr("id").split("_")[0];
	self.flagId = $(flag).attr("id").split("_")[1];
	
	self.roId = roId;
	self.count = 0;
	self.init = function(){
		var html = "<form id='aptRecommendation'>" + self.generateRow() + "</form>";
		html = html + "<button id='addRow' type='button' class='btn btn-success'>Add</button>"
		$(self.modalBody).html(html);
		$(self.modal).modal();
		self.bindEvents();
	}
	self.generateRow = function(){
		var html = 
				"<input type='text' name='"+self.count+"_name' placeholder='Recommendation'>" +
				"<input type='text' name='"+self.count+"_notes' placeholder='Add Notes'>" +
				"<input type='number' name='"+self.count+"_labor' placeholder='Labor Cost'>" +
				"<input type= 'number' name='"+self.count+"_parts' placeholder='Parts Cost'></br>" ;
		self.count++;
		return html;
	}
	self.bindEvents = function(){
		$("#addRow").on("click",function(){
			$("#aptRecommendation").append(self.generateRow);
		});
		$("#submitFlag").off("click");
		$("#submitFlag").on("click",function(){
			
			$("#aptRecommendation input").attr("style","");
			var emptyInputs = $('#aptRecommendation input').filter(function() { return this.value.trim() == ""; })
			emptyInputs.each(function(){
				if($(this).val() == ""){
					$(this).attr("style","border-color:red");
				}
			});
			if (emptyInputs.length > 0  ){
				$(emptyInputs[0]).focus();
				return false;
			}
			$(self.modal).modal("hide");
			var data  = {};
			 $("#aptRecommendation").find("input").each(function(){
				data[$(this).attr("name")] = $(this).val(); 
			});
			data["flagId"] = self.flagId;
			data["roId"] = self.roId;
			data["flagType"] = self.flagType;
//			setTimeout(function(){
//				ajaxRequest(window.update_flags_url,"GET",updateFlagResponse,data);
//			},300);
			setTimeout(function(){
				ajaxRequest(window.add_recommendations_url,"GET",updateFlagResponse,data);
			},300);
			
//			console.log(data);
			
		});
		
		
	}
}	
function CameraModal(canvasId){
	var self = this;
	self.modal = $("#camera_modal");
	self.canvas = $(canvasId)[0];
	self.camera = null;
	self.init = function(){
		var html = '<video id="video" width="320" height="240"  class="img-center" autoplay></video><canvas id="canvas" width="320" height="240" class="img-center" style= "display: none" ></canvas><div><button class="btn mr-10" id="snap">Snap Photo</button></div><button type="button" id="again" class="btn" style="display: none">Again</button></div>';
		$("#camera_modal_body").html(html);
		
		$("#canvas").hide();
		$("#video").show();
		$("#save").hide();
		$("#snap").click(function(){
			$("#canvas").show();
			$("#video").hide();
			$("#again").show();
			$("#save").show();
			$("#snap").hide();
			self.camera.capturePicture();
			/// add camera logic here
		});
		$("#again").off("click").on("click",function(){
			
			$("#canvas").hide();
			$("#video").show();
			$("#save").hide();
			$("#again").hide();
			$("#snap").show();
			
		});
		$("#save").click(function(){
			var vid = self.camera.getImage();
			self.canvas.getContext("2d").drawImage(vid, 0, 0, 320, 240);
			$(self.canvas).attr("data-image","true");
			self.camera.stop();
			self.modal.modal("hide");
		});
		$('#modal').on('hidden.bs.modal', function (e) {
			  // do something...
			  self.closeCamera();
			})
		self.modal.modal();
	
		self.camera = new CameraSnapShot();
		
		self.camera.setCanvas($("#canvas")[0]);
		self.camera.setVideo($("#video")[0]);
		self.camera.init();
		self.closeCamera = function(){
			self.camera.stop();
		}
	}
	
}
