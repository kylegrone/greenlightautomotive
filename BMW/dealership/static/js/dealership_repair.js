function DealershipRepair() {
	var self = this;
	dealership = new Dealership();
	
	
	this.services = [
	                
	                 ];
	this.type = ""; // 1 for service or Repair
	
	this.panel = ""; //panel that needs to be updated
	
	this.service_fetch_url = "";
	this.service_save_url = "";
	this.pagination_container= '#service-pagination';
	self.service_limit =12;
	self.current_page = 1;
	this.service_fetch_listener = [];
	this.select_listener = null;
	this.media_url = "";
	this.dealer_code;
	this.dealer_id;

	this.loading_div = $("#loading_page");
	self.service_class = "service_class";
	
	this.defaultTemplate = '<div class="col-sm-3 col-xs-6 mb-10 service_class">'+
                    '<div class="well">'+
                        '<div class="media">'+
                            '<div class="media-left">'+
                            '<a href=""><img class="media-object service_img img-thumbnail" src="" width="75"></a>'+
                            '</div>'+
                            '<div class="media-body">'+
                                '<p><span class="service_name"></span><br>DMS OPD Cod#: <span class="opd_code"></span><br>Duration: <span class="duration"></span> <br>Price:<span class="price_val"></span></p>'+
                                '<span class="hidden"><input type="hidden" class="service__id" /><input type="hidden" class="service__type" /><input type="hidden" class="service__flag" /></span>'+
                                '<div class="bg_wht pad-5 text-right">'+
                                	'<a class="button-service-delete" href="" data-toggle="modal" data-target=".deleterepair" class="text_grey"><span class="glyphicon glyphicon-trash"></span></a> &nbsp;'+ 
                                    '<a class="button-service-edit" href="" data-toggle="modal" data-target=".newrepair" class="text_grey"><span class="glyphicon glyphicon-pencil"></span></a>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>';
                
    this.edit_modal = '';

	this.getAddEditForm = function(id)
	{
		if(id == undefined){var data = {}; var callbackArguments = {};}
		else{var data = {"id":id}; var callbackArguments = {"id":id};}
		dealership.getTemplateFromServer(url_rservices_form, data, self.getAddEditFormCallback, callbackArguments);		
	};
	
	this.getAddEditFormCallback = function(content, callbackArguments){		
		$('#add-repair-modal .modal-body').html(content);
		if($("#id_flag_service").val() == "True"){
			$('.text_red').removeClass("hidden");
		}else{
			$('.text_grey').removeClass("hidden");			
		}
		
		if(callbackArguments.id == undefined){
            $("#id_type_1").attr("checked", "checked");			
		}else{
            $('#add-service-form #existing_id').attr('value',callbackArguments.id);
        }
		
        $("#type-container label:first").remove();        
		$('#add-service-form #id_dealer').attr('value',self.dealer_id);
		$('#add-repair-modal').modal("show");
	};
	
	this.getServicesList = function(search){
		self.panel = "#service-appointment";
		self.type = "s";
		self.pagination_container= '#service-pagination';
		var data = {'dealer_code': self.dealer_code};
        var callbackArguments = {"search" : search};
        var url = url_get_all_services;
        if(search != undefined){ url = url +"?search_text="+search; }
    	dealership.getDataFromServer(url, data, self.getServicesListCallback, callbackArguments);
	};
	
	this.getRepairsList = function(search){
		self.panel = "#repair-appointment";
		self.type = "r";
		self.pagination_container= '#repair-pagination';
		var data = {'dealer_code': self.dealer_code,'type':'r', "search_text" : search};
        var url = url_get_all_services;
        if(search != undefined){ url = url +"?search_text="+search; }
    	dealership.getDataFromServer(url, data, self.getRepairsListCallback);
	};
	
	this.getServicesListCallback = function(data, callbackArguments){
		self.loadData(data);
		self.getRepairsList(callbackArguments.search);
	};
	
	this.getRepairsListCallback = function(data, callbackArguments){
		self.loadData(data);
	};
	
	this.loadData = function(data){		
		console.info(data);
		self.services = data["services"];
		self.media_url = data["mainurl"];
		self.initialFill();
		self.loading_div.hide();
	};
	
	this.initialFill = function(){
		self.current_page = 1;
		self.fillPanel();
		self.setPaging();		
	};
	
	this.fillPanel = function(){
		$(self.panel).html("");
		var offset = self.getOffset();
		var count = 0;
		var added_count = 0;
		var row = '<div class="row"></div>';
		$.each(self.services,function(k,service){
			
					if(count >=offset){
						if (added_count< self.service_limit){
							console.info(count);
							if(count == 0){
								$(self.panel).append('<div class="row"></div>');
							}
							else if(count % 4 == 0){
								$(self.panel).append('<div class="row"></div>');								
							} 
							var service_template = $(self.defaultTemplate);
							if(service["image"]!=""){
								service_template.find(".service_img").prop("src",self.media_url+service["image"]);
							}
							service_template.find(".service_name").html(service["name"]);
							service_template.find(".duration").html(service["duration"]);
							service_template.find(".price_val").html(service["price_unit"]+service["price"]);	
							service_template.find(".opd_code").html(service["dms_opcode"]);
							service_template.find(".service__id").val(service["id"]);
							service_template.find(".service__type").val(service["type"]);
							service_template.find(".service__flag").val(service["type"]);
							$(self.panel+" .row:last").append(service_template);
							added_count++;
							
						}
						
					}
					count++;
		});	
		self.setActive();
	};
	
	this.setPaging = function(vehicles){
		var total_pages = self.getTotalPages();
		$(self.pagination_container).html("");
        alert(total_pages)
		if(total_pages>1){
			$(self.pagination_container).append(
					"<li class='prev_pagination'><a  aria-label='Previous'><span aria-hidden='true'>«</span></a></li>"		
			);
		}
		for (var i=1;i<=total_pages;i++){
				$(self.pagination_container).append("<li><a>"+i+"</a></li>");
		}
		if(total_pages>1){
			$(self.pagination_container).append(
					"<li class='next_pagination '><a  aria-label='Next'><span aria-hidden='true'>»</span></a></li>"		
			);
		}
		self.setActive();
	};
    
    this.setPaging = function(vehicles){
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
    this.setActive = function(){
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
	
	this.getOffset = function(){
		var total_pages = self.getTotalPages();
		var offset = ((self.current_page * self.service_limit) - self.service_limit) ;
		return offset;
	}
	
	this.getTotalPages = function(){
		var total_services = self.services.length;
		
		var total_pages = Math.ceil(total_services/self.service_limit) ;
		console.info(total_pages);
//		if(total_services % self.service_limit > 0){ 
//			total_pages++;
//		}
		return total_pages;
	}
	
	this.setEventListener = function(){
		$("body").on("click","#service-pagination li:not(.disabled), #repair-pagination li:not(.disabled)",function(){
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
		
		
		$('.button-service-add').click(function(){
			self.getAddEditForm();
		});
			
			
		$(document.body).on('submit', '#add-service-form', function(event) {
		    event.preventDefault();
		    var data = new FormData($(this).get(0));
		    window.dealershipRepair.createupdatesr(url_rservices_create_update, data);        
       		return false;
       		
		});  
		
		$(document.body).on('submit', '#delete-service-form', function(event) {
		    event.preventDefault();
		    $('.deleterepair').modal('hide');
		    window.dealershipRepair.deleteServiceOrRepair(url_rservices_delete, $(this).serialize());        
       		return false;
       		
		});
		
		$("body").off("click",".button-service-edit").on("click",".button-service-edit",function(){			
			self.getAddEditForm($(this).closest(".service_class").find(".service__id").val());
		});
		
		$("body").off("click",".button-service-delete").on("click",".button-service-delete",function(){			
			$("#delete-service-form").find(".form-service-id").val($(this).closest(".service_class").find(".service__id").val());	
		});
		
		$("body").off("click",".flag_icon").on("click",".flag_icon",function(){				
			$('.flag_icon').removeClass("hidden");	
			$(this).addClass("hidden");		
			if($(".text_grey").hasClass("hidden")){
				$("#id_flag_service").attr("value", "True");
			}else{
				$("#id_flag_service").attr("value", "False");
			}
		});
        
        
        $('#dealer-search-service').keypress(function(e){
            if(e.which == 13) {
                self.getServicesList($(this).val())
			}
		});
	};
	
	this.addNewServiceOrRepair = function(ajax_url, data){
		dealership.getDataFromServer(ajax_url, data, self.addNewServiceOrRepairCallback);
	};
	this.createupdatesr = function(ajax_url, data){
		dealership.createupdatesr(ajax_url, data, self.addNewServiceOrRepairCallback);
	};
	
	this.deleteServiceOrRepair = function(ajax_url, data){
		dealership.getDataFromServer(ajax_url, data, self.deleteServiceOrRepairCallback);
	};
	
	this.deleteServiceOrRepairCallback = function(data, callbackArguments){        
		self.getServicesList();	
	};
	
	this.addNewServiceOrRepairCallback = function(data, callbackArguments){
		if(data["status"] == "success"){                
            $('#add-service-form .alert-danger').html("");
            $('.newrepair').modal('hide');
            self.getServicesList();
        }
        else{
            $.each(data["errors"],function(name,value){
                $('#'+name+"_error").html(value);
            });
        }
		
	};
}