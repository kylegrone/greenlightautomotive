function AdvisorSelection(){
	this.advisors = [
	                 ];
	
	this.selected_advisor_id =null
	this.panel = "" //panel that needs to be updated
	this.appointment_id = "";
	this.advisor_fetch_url = "";
	
	this.dealer_code = ""
	this.advisor_save_url = "";
	this.pagination_container= null;
	var self = this;
	self.advisor_limit =10;
	self.current_page = 1;
	this.service_fetch_listener = []
	this.select_listener = null
	this.media_url = ""
	var self = this;
	this.loading_div = $("#loading_page");
	self.advisor_class = "advisor_class";
	this.save_on_select = true
	self.profile_id = 0
	self.save_success_callback = null;
	self.type = "appointment" //could be user or appoointment 
	self.default_image = "/noimage.gif";
	this.defaultTemplate = '<li class="'+this.advisor_class+'"><a href="#"><img class="advisor_img " src="" width="130" height="120">'+
    '<div class="clear pad-5"></div>'+
    '<i class="fa fa-check fa-2x"></i> <span class="advisor_name"></span><div class="pad-10"></div></a><input type="hidden" class="advisor__id" value=""/></li>	';
	
	
//	this.defaultTemplate = '<div class="col-sm-3 col-xs-6 mb-10 '+this.advisor_class+'" data-id="1">'+
//		'<div class="well">'+
//    		'<div class="media">'+
//        		'<div>'+
//            		'<a href="#">'
//        				+'<img class="media-object advisor_img img-thumbnail" src="" width="95%" height="100px"></a>'+
//            	'</div>'+
//            	'<div class="media-body">'+
//            		'<p><span class="service_name"></span><br> <span class="advisor_name"></span>'+
//            		'<span class="button-checkbox">'+
//			        	'<button type="button" class="btn_selection btn btn-grey btn-sm btn-block btn-default" data-color="success">'+
//                 			'<i class="state-icon glyphicon glyphicon-unchecked"></i> Select</button>'+
//                 			'<input type="hidden" class="advisor__id" value=""/>'+
//                 	'</span>'+
//                 '</div>'+
//               
//             '</div>'+
//         '</div>'+
//     '</div>';
//		;	
		
	
	
	this.selectListener = []// this is the list of callbacks that is called on seletion of an advisor
		
	this.setTemplate = function(template){
		this.defaultTemplate = template;
	}
	
	/* this method is used to check if the advisor is added */
	this.checkAdvisorAdded = function(advisor){
		var current_id = advisor.find(".advisor__id").val();
		
		var exists = false;
		if(self.selected_advisor_id == current_id){
			exists = true
		}else if (current_id =="" && self.selected_advisor_id ==null ){
			exists = true
		}
		
		return exists
	}
	
	/* this method is used after the fill to select the default advisor */
	this.selectFromAdvisors = function(){
		$(self.panel+" ."+self.advisor_class).each(function(){
			var advisor = $(this);
			if (self.checkAdvisorAdded(advisor)!=false){
				self.selectAdvisor(advisor,true);
			}
		})
	}
	
	/*params
	 * advisor: advisor grid that need to e selected
	 * dont_save: its passed to check if need to save to the server
	 * */
	this.selectAdvisor = function(advisor,dont_save){
		self.unselectAdvisor();
		advisor.addClass("active");
		if(self.checkAdvisorAdded(advisor)==false){
			if(advisor.find(".advisor__id").val()==""){
				self.selected_advisor_id=null
			}else{
				self.selected_advisor_id = advisor.find(".advisor__id").val()
			}
		}
		if (self.save_on_select && typeof dont_save=="undefined"){
			this.saveAdvisor(advisor) 
		}
	}
	

	/* this metho dis used to deselect the advisor and also save it to the server */
	this.deleteAdvisor = function(advisor){
		var advisor__id = advisor.find(".advisor__id").val();
		advisor.removeClass("active");

		self.selected_advisor_id = null 
		
		if (self.save_on_select){
			this.saveAdvisor() 
		}
		
	}
	/* this method is used to unselect all advisors*/
	this.unselectAdvisor = function(){
		self.selected_advisor_i = null
	
		$(self.panel+" ."+self.advisor_class).removeClass("active");
				
	}
	
	/* this is the method called for the intial fill of the advisor. called on all the new reques*/
	self.initialFill = function(){
		self.current_page = 1;
		self.fillPanel();
		self.setPaging();
		self.setEventListener();
		
	}
	
	
	this.fillAnyAdvisor = function(){
		var advisor_template = $(self.defaultTemplate);
		advisor_template.find(".advisor_img").prop("src",self.media_url+self.default_image);
		advisor_template.find(".advisor_name").html("Any Advisor");
		advisor_template.find(".advisor__id").val("")
		advisor_template.find(".advisor__id").addClass("anyadvisor")
		$(self.panel).find(".select_advisor").append(advisor_template);
		
	}
	/* this methhod is used to fill the panel with advisors.it is called when page is changed also*/
	this.fillPanel = function(){
		self.unselectAdvisor();
		$(self.panel).html("<ul class='select_advisor'></ul>")
		self.fillAnyAdvisor()
		var offset = self.getOffset();
		var count = 0;
		var added_count = 0;
		
		
		$.each(self.advisors,function(k,advisor){
					if(count >=offset){
						if (added_count< self.advisor_limit){
							var advisor_template = $(self.defaultTemplate);
							if(advisor["userprofile__avatar"]!=""){
								advisor_template.find(".advisor_img").prop("src",self.media_url+advisor["userprofile__avatar"]);
							}else{
								
								advisor_template.find(".advisor_img").prop("src",self.media_url+self.default_image);
							}
							
							advisor_template.find(".advisor_name").html(advisor["first_name"]+" "+advisor["last_name"]);
							advisor_template.find(".advisor__id").val(advisor["id"])
							$(self.panel).find(".select_advisor").append(advisor_template);
							added_count++;
						}
					}
					count++;
		});	
		self.selectFromAdvisors();
		self.setActive();
	
	}
	
	
	/* this method is used to set the pagination controls*/
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
	
	/* this method sets the pagination active controle. based on the current page*/
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
	/* this metnod gets the current offset of the pagingg*/
	self.getOffset = function(){
		var total_pages = self.getTotalPages();
		var offset = ((self.current_page * self.advisor_limit) - self.advisor_limit) ;
		return offset;
	}
	/* this returns the total number of pages based on the lenth and limit */
	self.getTotalPages = function(){
		var total_advisors = self.advisors.length;
		var total_pages = Math.ceil(total_advisors/self.advisor_limit) ;
		return total_pages;
	}
	
	/* this registers the dom events*/
	self.setEventListener = function(){
		/* this triggers the page change event and sets the current page and fills the panel*/
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
		
		/* this triggers the seletion of an advisor*/
		$("body").on("click",self.panel+" ."+self.advisor_class,function(event){
			event.preventDefault();
			var advisor = $(this).closest("."+self.advisor_class);
			var id = advisor.data("id");
			if(self.checkAdvisorAdded(advisor)!=false){
				self.deleteAdvisor(advisor);
			}else{
				self.select_listener(advisor);
			}
			
		});
		
	}
	
	/* this methd is used to fetch all the advisors from the server and start the intial call */
	this.setAdvisors = function(){
		self.loading_div.show()
		
		$.ajax({
				"url":self.advisor_fetch_url,
				
				"data":{
					"appointment_id":self.appointment_id,
					"type":self.type,
					"dealer_code":self.dealer_code,
					"profile_id":self.profile_id
				},
				"success":function(data){
					self.advisors = data["advisors"];
					console.info(data["selected_advisor"] )
					self.selected_advisor_id =data["selected_advisor"] ;
					self.media_url = data["mainurl"]
					$.each(self.service_fetch_listener,function(k,v){
						v(data["advisors"],data["selected_advisor"]);
					});
					self.initialFill()
					self.loading_div.hide();
				},"error":function(){
					self.loading_div.hide();
				}
		})
	}
	
	/* this method is used to save the advisor on the ther server */
	this.saveAdvisor = function(saveAdvisor){
		self.loading_div.show();
		
		$.ajax({
				"url":self.advisor_save_url,
				
				"data":{
					"appointment_id":self.appointment_id,
					"type":self.type,
					"dealer_code":self.dealer_code,
					"advisor_id":self.selected_advisor_id,
					"profile_id":self.profile_id
				},
				"success":function(data){
						if(data["success"]==false){
							alert("Error saving Advisor");
						}
						self.loading_div.hide();
						if(typeof self.save_success_callback!="undefined" && self.save_success_callback!=null){
							
							self.save_success_callback(saveAdvisor)
						}
						
				},"error":function(){
					alert("Error saving Advisor");
					self.loading_div.hide();
				}
		})
	}
}