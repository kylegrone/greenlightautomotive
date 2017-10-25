function ServiceSelection(){
	this.services = [
	                
	                 ];//all the services
	this.search_box = "services_search_box";
	this.type = "s"; // 1 for service or Repair
	this.selected_services_id = [
	                             ]
	this.panel = "" //panel that needs to be updated
	this.appointment_id = "";
	this.service_fetch_url = "";
	
	this.dealer_code = ""
	this.service_save_url = "";
	this.pagination_container= null;
	var self = this;
	self.service_limit =12;
	self.current_page = 1;
	this.service_fetch_listener = []
	this.select_listener = null
	this.media_url = ""
	var self = this;
	this.loading_div = $("#loading_page");
	self.service_class = "service_class";
	this.save_on_select = true
	self.not_sure_listener = null;
	self.after_save_fn = null;
	self.select_text="Select";
	self.unselect_text = "Unselect";
	self.detail_modal = ""
	self.description_modal = ""
	self.defaultTemplate = ""
	self.default_image="noimage.gif";
	self.jquery_conflict =true;
	this.initiate =function(){
		this.setTemplates()
		this.setServices();
	}
	
	
	this.setTemplates = function(){
		 self.detail_modal = '<div class="modal service_detail_modal fade" tabindex="-1" role="dialog" id=""  >'+
		  '<div class="modal-dialog">'+
		    '<div class="modal-content">'+
		      //'<div class="modal-header">'+
		        //'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
		      		//	'<span aria-hidden="true">&times;</span></button>'+
		       
		      //'</div>'+
		      
		      '<div class="modal-body">'+
		      	'<div class="title-service-modal"><img height="60px" width="60px" class="detail_service_img"/>&nbsp;&nbsp;<span class="modal-title"></span></div>'+
		        '<h4 class="modal_desc"></h4>'+
		        		'Add Additional Information for our service Advisor (optional)<br/><br/><textarea rows="5" placeholder="Add Comment"class="modal_note form-control"></textarea>'+
		      '</div>'+
		      '<div class="modal-footer">'+
		      		'<div class="row"><div class="col-sm-3">Not Sure? <a class="pointer not_sure_link">Click here</a></div></div>'+
		      		'<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'+
		      		'<button type="button" class="btn btn-success add_cart" data-service_id="">'+self.select_text+'</button>'+
		      '</div>'+
		     
		    '</div><!-- /.modal-content -->'+
		  '</div><!-- /.modal-dialog -->'+
		'</div><!-- /.modal -->';


			self.description_modal = '<div class="modal service_description_only_modal fade" tabindex="-1" role="dialog" id=""  >'+
			'<div class="modal-dialog">'+
			'<div class="modal-content">'+
			'<div class="modal-header">'+
			'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
				'<span aria-hidden="true">&times;</span></button>'+
			'<h4 class="modal-title"></h4>'+
			'</div>'+
			'<div class="modal-body">'+
			
			'<h4 class="modal_desc"></h4>'+
			
			'</div>'+
			'<div class="modal-footer">'+
			'<div class="row"><div class="col-sm-3">Not Sure? <a class="pointer not_sure_link">Click here</a></div></div>'+
			'<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'+
			'</div>'+
			
			'</div><!-- /.modal-content -->'+
			'</div><!-- /.modal-dialog -->'+
			'</div><!-- /.modal -->';
			
			self.defaultTemplate = '<div class="col-sm-3 col-xs-6 mb-10 service_and_repair_containers '+this.service_class+'" data-id="1">'+
			'<div class="well">'+
			'<div class="media">'+
			'<div class="media-left">'+
			'<a href="#" >'
				+'<img class="media-object service_img img-thumbnail imgpopup" src="" width="40px" height="40px"/></a>'+
			'</div>'+
			'<div class="media-body">'+
			
			'<p class="service_name_container"><span class="service_name"></span><br/><div class="servicedtlabels">OPD code: '+
			'<span class="opd_code"></span></div><div class="servicedtlabels">Duration:  <span class="duration"></span></div>'+
			' <div class="servicedtlabels">Price: <span class="price_val"></span></div></p>'+
			'<div style="padding-top:20px"></div>'+
			'<div class="row">'+
				'<div class="col-sm-4"><a class="pointer detail_selector" style="padding-top:5px">Detail</a></div>'+
				'<div class="col-sm-8">'+
			   	'<span class="button-checkbox">'+
			      	'<button type="button" class="btn_selection btn btn-grey btn-sm btn-block btn-success" data-color="success">'+
			   			'<i class="state-icon "></i> '+self.select_text+'</button>'+
			   			'<input type="hidden" class="service__id" value=""/>'+
			   	'</span>'+
				'</div>'+
			'</div>'+
			'</div>'+
			'<div class="service_description" style="display:none"></div>'
			'</div>'+
			'</div>'+
			'</div>';
			;	
	}
	this.selectListener = []// this is the list of callbacks that is called on seletion of a  service
	this.detailListener = []//this is the listener used to callback select
	this.setTemplate = function(template){
		this.defaultTemplate = template;
	}
	
	this.checkServiceAdded = function(service){
		var current_id = service.find(".service__id").val();
		var exists = false;
		$.each(self.selected_services_id,function(key,service_db){
			if(service_db["service__id"] ==current_id){
				exists = service_db
			}
		});
		return exists
	}
	
	
	this.selectServices = function(){
		$(self.panel+" ."+self.service_class).each(function(){
			var service = $(this);
			if (self.checkServiceAdded(service)!=false){
				self.selectService(service);
			}
		})
	}
	
	
	this.selectService = function(service,note){
		service.find(".btn_selection").addClass("btn-danger");
		service.find(".btn_selection").removeClass("btn-success");
		service.find(".btn_selection").html(self.unselect_text)
//		service.find(".btn_selection i").removeClass("glyphicon-unchecked");
//		service.find(".btn_selection i").addClass("glyphicon-ok");
		if(self.checkServiceAdded(service)==false){
			self.selected_services_id.push({"service__id":service.find(".service__id").val(),"note":note})
		}
		if (self.save_on_select){
			this.saveServices() 
		}
		
	}
	
	this.showDesriptionModal = function(service){
		/* this is used to display add to cart information*/
		var desc = service.find(".service_description").html();
		var title  = service.find(".service_name").html();
		var img  = service.find(".service_img");
		var service_db = self.checkServiceAdded(service);
		var comment = "";
		if(service_db){
			comment = service_db["note"];
		}
		
		$(self.panel).find(".service_detail_modal").find(".modal_note").val("")
		$(self.panel).find(".service_detail_modal").find(".modal_desc").html(service.find(".service_description").html());
		$(self.panel).find(".service_detail_modal").find(".modal-title").html(service.find(".service_name").html());
		$(self.panel).find(".service_detail_modal").modal('show');
		$(self.panel).find(".service_detail_modal").find(".detail_service_img").attr("src",img.attr("src"));
		$("body").on("click",self.panel+" .service_detail_modal .add_cart",function(){
			var comment = $(self.panel).find(".service_detail_modal .modal_note").val();
			self.selectService(service,comment);
			$(self.panel).find(".service_detail_modal").modal('hide');
		});
	}
	
	this.showDesriptionOnlyModal = function(service){
		var desc = service.find(".service_description").html();
		var title  = service.find(".service_name").html();
		var img  = service.find(".service_img");
		var service_db = self.checkServiceAdded(service);
		$(self.panel).find(".service_description_only_modal").find(".modal_desc").html(service.find(".service_description").html());
		$(self.panel).find(".service_description_only_modal").find(".modal-title").html(service.find(".service_name").html());
		$(self.panel).find(".service_description_only_modal").modal('show');
		
		 $(self.panel).find(".service_description_only_modal").find(".model_img").src(service.find(".service_img").src());
		 
	}
	
	this.closeDesriptionOnlyModal =function(){
		$(self.panel).find(".service_description_only_modal").modal('hide');
	}
	this.closeDesriptionModal =function(){
		$(self.panel).find(".service_detail_modal").modal('hide');
	}
	
	/* this is used to deselct the service and save it to the server */
	this.deSelectService = function(service){
		
		var service__id = service.find(".service__id").val();
		service.find(".btn_selection").removeClass("btn-danger");
		service.find(".btn_selection").addClass("btn-success");
		service.find(".btn_selection").html(self.select_text);
//		service.find(".btn_selection i").addClass("glyphicon-unchecked");
//		service.find(".btn_selection i").removeClass("glyphicon-ok");
		
		var remove_index = null
		
		$.each(self.selected_services_id,function(k,v){
				if(service__id == self.selected_services_id[k]["service__id"]){
					remove_index = k
				}
		}); 
		if(remove_index !=null){
			self.selected_services_id.splice(remove_index,1);
		}
		if (self.save_on_select){
			this.saveServices() 
		}
		
	}
	
	/* this method is used to unselect all services*/
	this.unselectServices = function(){
		$(self.panel+" ."+self.service_class).find(".btn_selection").removeClass("btn-success");
		$(self.panel+" ."+self.service_class).find(".btn_selection i ").removeClass("glyphicon-ok"); 
		$(self.panel+" ."+self.service_class).find(".btn_selection i ").addClass("glyphicon-unchecked");		
				
	}
	
	
	/* this is called when data is fetched first time*/
	self.initialFill = function(){
		self.current_page = 1;
		self.fillPanel();
		self.setPaging();
		self.setEventListener();
		
	}
	
	
	/* this function is used to fill the services in the panel*/
	this.fillPanel = function(){
		self.unselectServices();
		$(self.panel).html("")
		var offset = self.getOffset();
		var count = 0;
		var added_count = 0;
		$.each(self.services,function(k,service){
					if(count >=offset){
						if (added_count< self.service_limit){
							var service_template = $(self.defaultTemplate);
							if(service["image"]!="" && service["image"]!=null && service["image"]!="null"){
								service_template.find(".service_img").prop("src",self.media_url+service["image"]);
							}
							else{
								service_template.find(".service_img").prop("src",self.media_url+self.default_image);
								
							}
							service_template.find(".service_name").html(service["name"]);
							service_template.find(".duration").html(service["duration"]);
							service_template.find(".price_val").html(service["price_unit"]+service["price"]);	
							service_template.find(".opd_code").html(service["dms_opcode"]);
							service_template.find(".service_description").html(service["description"]);
							service_template.find(".service__id").val(service["id"])
							$(self.panel).append(service_template);
							added_count++;
						}
					}
					count++;
		});	
		self.selectServices();
		self.setActive();
		$(self.panel).append(self.detail_modal);
		$(self.panel).append(self.description_modal);
		//if(self.jquery_conflict){
			//jQuery.noConflict();
		//}
		$(self.panel).find(".service_detail_modal").modal({ show: false})
		    
		
	}
	
	
	self.setPaging = function(vehicles){
		var total_pages = self.getTotalPages();
		$(self.pagination_container).html("")
		if(total_pages>1){
			$(self.pagination_container).append(
					"<li class='prev_pagination'><a  aria-label='Previous'><span aria-hidden='true'>«</span></a></li>"		
			)
		}
		for (var i=1;i<=total_pages;i++){
				$(self.pagination_container).append("<li><a>"+i+"</a></li>");
		}
		
		if(total_pages>1){
				$(self.pagination_container).append(
						"<li class='next_pagination '><a  aria-label='Next'><span aria-hidden='true'>»</span></a></li>"		
				)
		}
		self.setActive();
	}
	
	/*this is used to set page active */
	self.setActive = function(){
		$(self.pagination_container+" li").removeClass("active");
		var total_pages = self.getTotalPages();
		$(self.pagination_container+" li").each(function(k,v){
			if($(this).text()==self.current_page){
				$(this).addClass("active");
			}
		})
		if(self.current_page == total_pages){
			$(self.pagination_container+" li.next_pagination").addClass("disabled");
		}else{
			$(self.pagination_container+" li.next_pagination").removeClass("disabled");
		}
		if(self.current_page == 1){
			$(self.pagination_container+" li.prev_pagination").addClass("disabled");
		}else{
			$(self.pagination_container+" li.prev_pagination").removeClass("disabled");
		}
	}
	self.getOffset = function(){
		var total_pages = self.getTotalPages();
		var offset = ((self.current_page * self.service_limit) - self.service_limit) ;
		return offset;
	}
	
	self.getTotalPages = function(){
		var total_services = self.services.length;
		
		var total_pages = Math.ceil(total_services/self.service_limit) ;
		console.info(total_pages);
//		if(total_services % self.service_limit > 0){ 
//			total_pages++;
//		}
		return total_pages;
	}
	
	self.setEventListener = function(){
		$("body").on("click",self.pagination_container+" li:not(.disabled)",function(){
			
			if($(this).hasClass("next_pagination")){
				var current_page = parseInt(self.current_page) + 1
			}else if($(this).hasClass("prev_pagination")){
				var current_page = parseInt(self.current_page) - 1
			}else{
				var current_page = $(this).text();
			}
			self.current_page = current_page;
			self.fillPanel();
			var total_pages = self.getTotalPages();
			self.setActive();
		
		});
		
		$("body").on("click",self.panel+" .btn_selection",function(){
			var service = $(this).closest("."+self.service_class);
			
			var id = service.data("id");
			if(self.checkServiceAdded(service)!=false){
				self.deSelectService(service);
			}else{
				self.select_listener(service);
			}
			console.info(self.selected_services_id)
		});
		
		$("body").on("click",self.panel+" .detail_selector",function(){
			var service = $(this).closest("."+self.service_class);
			console.info(service);
			var id = service.data("id");
			self.showDesriptionModal(service)
			
		});
		
		$("body").on("click",self.panel+" .not_sure_link",function(){
			self.closeDesriptionOnlyModal();
			self.closeDesriptionModal();
			if(self.not_sure_listener){
				self.not_sure_listener()
			}
			
		});
		
		$(self.search_box). keypress(function(e){//on("click",self.panel+" "+self.search_box,function(){
				
//				if($(this).val()!=""){
					 if(e.which == 13) {
						 self.setServices($(this).val())
					    }
//				}
		})
		
	}
	
	self.removeItem =function (array, item){
	    for(var i in array){
	        if(array[i]==item){
	            array.splice(i,1);
	            break;
	            }
	    }
	}
	
	/* this is used to get all services */
	this.setServices = function(search){
		self.setTemplates()
		var search_text = ""
		if(typeof search!="undefined"){
			search_text = search
		}
		self.loading_div.show()
		$.ajax({
				"url":self.service_fetch_url,
				"data":{
					"appointment_id":self.appointment_id,
					"type":self.type,
					"dealer_code":self.dealer_code,
					"search_text":search_text
				},
				"success":function(data){
					self.services = data["services"];
					self.selected_services_id =data["selected_services_id"] ;
					self.media_url = data["mainurl"]
					$.each(self.service_fetch_listener,function(k,v){
						v(data["services"],data["selected_services_id"]);
					});
					self.initialFill()
					self.loading_div.hide();
				},"error":function(){
					self.loading_div.hide();
				}
		})
	}
	
	/* this is used to save serices to the server */
	this.saveServices = function(){
		self.loading_div.show()
		console.info(self.selected_services_id)
		$.ajax({
				"url":self.service_save_url,
				
				"data":{
					"appointment_id":self.appointment_id,
					"type":self.type,
					"dealer_code":self.dealer_code,
					"services":JSON.stringify(self.selected_services_id)
				},
				"success":function(data){
						if(data["success"]==false){
							alert("Error saving");
						}else{
							if(self.after_save_fn !=null){
								
								self.after_save_fn()
							}
						}
						self.loading_div.hide();
				},"error":function(){
					alert("Error saving");
					self.loading_div.hide();
				}
		})
	}
}