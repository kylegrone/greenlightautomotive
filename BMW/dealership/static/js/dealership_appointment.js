function DealershipAppointment() {
	var self = this;
	dealership = new Dealership();
	//var dealershipOverview = new DealershipOverview();
	this.selectedTimeSlot = null;
	this.selected_vehicle = null;
	
	this.search;
	this.criteria;
	this.panel;
	this.flow = "update";
	this.cust_id;
	this.appt_id = null;
	this.vehicle_id = null;
	this.dealer_id;
	this.dealer_code;
	this.way_away_save_callback = null;
	this.date_save_callback = null;
	this.setEventListeners = function(){	
		
		$(document.body).on('submit', '.appointment-page #searchcust_form', function(event) {
		    event.preventDefault();
		    var data = $(this).serializeArray();
		    window.dealershipOverview.overviewTimeDailySearch(data[0].value, data[1].value);
       		return false;
		}); 
		
		$(document.body).on('click', '#appointment .fa-plus-circle', function(event) {
			//dealershipOverview.appt_id = self.appt_id;
			window.dealershipOverview.setOverviewFilters();	
		}); 			
			
		$(document.body).on('click', '#customer-appointment .fa-plus-circle', function(event) {
			var panel_id = "#customer-appointment";				
		    self.getCustomerForAppointment(panel_id, self.cust_id, self.dealer_code);	
		}); 
		
		$(document.body).on('click', '#repair-appointment .fa-plus-circle', function(event) {
			var panel_id = "#repair-appointment";
			//self.getServicesForAppointment(url_appointment_services, panel_id, appt_id);
			self.getServicesForAppointment(self.appt_id);
		}); 

		$(document.body).on('click', '#wayaway-appointment .fa-plus-circle', function(event) {
			var panel_id = "#wayaway-appointment";
			var panelObject = {'cust_id':self.cust_id, 'panel_id':panel_id, 'callback':self.saveWayAwayForAppointmentCallback};
			self.getWayAwayForAppointment(url_appointment_wayaway, self.appt_id, panelObject);	
		}); 
		
		$(document.body).on('click', '#time-appointment .fa-plus-circle', function(event) {
			var panel_id = "#time-appointment";
			self.getTimeForAppointment(url_appt_update_time_template, self.appt_id, {'panel_id':panel_id, 'callback':self.timeSelectionCallback});
		}); 
		
		$(document.body).on('click', '.carousel-linked-nav > li > a', function(event) {
			var element = $(this).parent().attr("rel");
		    var item = Number($(this).attr('href').substring(1));
		    $(element).carousel(item);
		    $(element+' .carousel-linked-nav .active').removeClass('active');
		    $(this).parent().addClass('active');
		    return false;
		});
		
		
		/*
		$(document.body).on('click', '.carousel-control', function(event) {
			var element = $(this).attr("href");
			console.info(element);
			$(element+' .carousel-linked-nav .active').removeClass('active');
        	var idx = $(element+' .item.active').index();        
        	
        	if($(this).hasClass("right")){
        		idx = idx + 1;
        		if(!($(element+' .carousel-linked-nav li:eq(' + idx + ')').length > 0)){
        			idx = 0;
        		}
        	}
        	else
        	{
        		idx = idx - 1;
        		if(!($(element+' .carousel-linked-nav li:eq(' + idx + ')').length > 0)){
        			idx = $(element+' .carousel-linked-nav li a').length;
        		}
        	}
        	console.info(idx);
        	$(element+' .carousel-linked-nav li:eq(' + idx + ')').addClass('active');
		});
		*/
	};

	//open the panel according to the panel query passed in url
	this.switchAccordian = function(open)
	{
		$('.panel-collapse').addClass("collapse");
		$(open+" .panel-collapse").removeClass("collapse");
		$(open+" .panel-title a").removeClass("collapsed");
		$(open+" .fa").removeClass("fa-plus-circle").addClass("fa-minus-circle");		
	};
	
	//binds all the events required for customer vehicle selection panel
	// -- advisor selection
	// -- remove vehicle
	// -- select for appointment
	//gets the customer template from server along with customer vehicle data
	this.getCustomerForAppointment = function(panel_id, cust_id, dealer_code){	
		$(document.body).off('click', panel_id+' .create_appointment').on('click', panel_id+' .create_appointment', function(event) {
			var advisor_id = $(this).closest('.customer_vehicle').find(".advisor-panel p").attr("rel");	
			if($(this).attr("appt_id") != ""){
				window.location = url_appointment+"?panel=customer&customer_id="+cust_id+"&vehicle_id="+$(this).attr("rel")+"&appointment_id="+$(this).attr("appt_id"); 
			}
			else
			{
				var data = {'customer_id':cust_id, 'vehicle_id':$(this).attr("rel"), "advisor_id":advisor_id};
				var callbackArguments = {'customer_id':cust_id, 'vehicle_id':$(this).attr("rel")};
				self.createCustomerAppointment(data, self.createCustomerAppointmentCallback, callbackArguments);	
			}
							
		}); 
		
		$(document.body).off('click', panel_id+' .remove_vehicle').on('click', panel_id+' .remove_vehicle', function(event) {
			self.removeCustomerVehicle($(this).attr("rel"), $(this).attr("cust_id"));
            $(this).closest( ".well" ).remove();
		});  
		
		$(document.body).on('submit', '#editcustomerform', function(event) {
			event.preventDefault();
			var data = $(this).serializeArray();
			var name = $(this).find('input[name="first_name"]').val()+" "+$(this).find('input[name="last_name"]').val() ;
			callbackArguments = {'panel_id': panel_id,'user_id':cust_id,'name':name};
		    dealership.getDataFromServer(url_customer_edit, data, self.getCustomerEditCallback, callbackArguments);
       		return false;		
		});
					
		$(document.body).off('click', panel_id+' .edit-advisor').on('click', panel_id+' .edit-advisor', function(event) {
			//$(panel_id+" .customer_vehicle").removeClass("selectedVehicle");			
			//$(this).closest(".customer_vehicle").addClass("selectedVehicle");	
			//event.preventDefault();
			
			self.selected_vehicle = $(this);
			var advisor_selection = new AdvisorSelection();
			var type=$(this).data("adtype")
			var customer=$(this).data("customer")
			advisor_selection.select_listener = self.selectAdvisor;
			
			if(typeof type !="undefined" && type=="user" && typeof customer !="undefined" ){
				advisor_selection.type = "user";
				advisor_selection.select_listener = advisor_selection.selectAdvisor;
				advisor_selection.selected_advisor_id = $(this).attr("rel")
				advisor_selection.profile_id = customer
				advisor_selection.save_success_callback =  self.closeAdvisor;
				
			}else if(typeof type !="undefined" && type=="appointment" ){
				advisor_selection.type = "appointment";
				advisor_selection.select_listener = advisor_selection.selectAdvisor;
				advisor_selection.selected_advisor_id = $(this).attr("rel")
				
				advisor_selection.save_success_callback =  self.closeAdvisor;
			}
			advisor_selection.panel = "#advisor-appointment";
			advisor_selection.dealer_code = dealer_code;
			advisor_selection.pagination_container = "#advisor_pagination";
			if(self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel input").val() != "")
			advisor_selection.appointment_id = self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel input").val();
			
			advisor_selection.advisor_fetch_url = url_get_all_advisors_ajax;
			advisor_selection.advisor_save_url = url_save_advisor_ajax;
			advisor_selection.setAdvisors();
			//return false;
			
		}); 
		
		$(document.body).off('click', panel_id+' .edit-advisor2').on('click', panel_id+' .edit-advisor2', function(event) {
			//$(panel_id+" .customer_vehicle").removeClass("selectedVehicle");			
			//$(this).closest(".customer_vehicle").addClass("selectedVehicle");	
			//event.preventDefault();
			
			self.selected_vehicle = $(this);
			var advisor_selection = new AdvisorSelection();
			var type=$(this).data("adtype")
			var customer=$(this).data("customer")
			advisor_selection.select_listener = self.selectAdvisor;
			console.info(type)
			if(typeof type !="undefined" && type=="user" && typeof customer !="undefined" ){
				advisor_selection.type = "user";
				advisor_selection.select_listener = advisor_selection.selectAdvisor;
				advisor_selection.selected_advisor_id = $(this).attr("rel")
				advisor_selection.profile_id = customer
				advisor_selection.save_success_callback =  self.closeAdvisor;
				
			}
			advisor_selection.panel = "#advisor-appointment";
			advisor_selection.dealer_code = dealer_code;
			advisor_selection.pagination_container = "#advisor_pagination";
			if(self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel input").val() != "")
			advisor_selection.appointment_id = self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel input").val();
			
			advisor_selection.advisor_fetch_url = url_get_all_advisors_ajax;
			advisor_selection.advisor_save_url = url_save_advisor_ajax;
			advisor_selection.setAdvisors();
			//return false;
			
		}); 

		
		$(document.body).off('click', '#select-advisor-modal').on('click', '#select-advisor-modal', function(event) {
										
		}); 
		
		$(document.body).off('click', '#select-advisor-modal .modal-body a').on('click', '#select-advisor-modal .modal-body a', function(event) {
												
		}); 
				
		var data = {'user_id':cust_id};
		if(self.vehicle_id != null){ data['vehicle_id'] = self.vehicle_id;  }
		if(self.appt_id != null){ data['appointment_id'] = self.appt_id;  }
		callbackArguments = {'panel_id': panel_id};
		dealership.getTemplateFromServer(url_appointment_customer, data, self.getCustomerForAppointmentCallback, callbackArguments);
	};
	

	this.selectAdvisor = function(advisor,dont_save){
		console.info(self.selected_vehicle);
		self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel p").attr("rel", advisor.find(".advisor__id").val());
		self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel p").html("Advisor: <br>"+advisor.find(".advisor_name").html());
		if(self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel input").val() != ""){
			var data = {'id':self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel input").val(), 'advisor_id':advisor.find(".advisor__id").val()};
			self.createCustomerAppointment(data,self.changeAdvisorCallback);
		}
		else
		{
			$('#select-advisor-modal').modal('hide');
		}
				
		//$(panel_id+" .selectedVehicle .advisor-panel p").attr("rel", $(this).attr('rel'));
		//$(panel_id+" .selectedVehicle .advisor-panel p").html("Advisor: <br>"+$(this).html());	
	};
	this.closeAdvisor = function(advisor,dont_save){
		
		
		self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel p").attr("rel", advisor.find(".advisor__id").val());
		self.selected_vehicle.closest('.customer_vehicle').find(".advisor-panel p").html("Advisor: <br>"+advisor.find(".advisor_name").html());
		self.selected_vehicle.closest('.customer_vehicle').find(".media-left .img-thumbnail").attr('src',(advisor.find(".advisor_img ").attr("src")));
		
		
		$('#select-advisor-modal').modal('hide');
	}
	this.changeAdvisorCallback = function(data, callbackArguments){
		$('#select-advisor-modal').modal('hide');
		//alert("advisor changed");
	};
	
	this.getCustomerEditCallback = function(response,callbackArgument){
		if(response["success"]==true){
			$('.cuseditname-'+callbackArgument.user_id).html(callbackArgument.name);
			var data = {'user_id': callbackArgument.user_id};
			dealership.getTemplateFromServer(url_appointment_customer, data, self.getCustomerForAppointmentCallback, {'panel_id':callbackArguments.panel_id});
			$('.editcust').modal('toggle');
			$('.modal-backdrop').removeClass('in');
			}else{
    		if (Object.prototype.toString.call(response["message"]) === '[object Array]'){
	    		var errmsg = "<ul>";
	    		for(i=0; i<response["message"].length; i++){
	    			$('input[name="'+response["message"][i][0]+'"]').addClass('inputTxtError');
	    			errmsg += "<li>"+response["message"][i][1]+"</li>";
	    		}
	    		errmsg +="</ul>";
    		}
    		else{
    			errmsg = response["message"]
    		}
             $('.errmsg').html(errmsg);
             $('.alert-danger').show();
    	}
		
	};
	//call back registered for customer vehicle template ajax call
	this.getCustomerForAppointmentCallback = function(response, callbackArguments){
		$(callbackArguments.panel_id+" .ajax-content").html(response);	
	};

	//ajax call to remove cusotomer vehicle
    this.removeCustomerVehicle = function(cust_vehicle_id, cust_id){
    	var data = {'cust_veh_id':cust_vehicle_id};
    	var callbackArguments = {'cust_id':cust_id};
    	dealership.getDataFromServer(url_appt_cust_veh_del, data, self.removeCustomerVehicleCallback, callbackArguments);
    };	
    
    this.removeCustomerVehicleCallback = function(data, callbackArguments){
    	var panel_id = "#customer-appointment";	
		self.getCustomerForAppointment(panel_id, callbackArguments.cust_id, self.dealer_code);
    };
    
    //--create appointment if no appointment id is provided
    //--updates appointment if appointment id is provided
    //--optional callback function can be passed from calling location
    this.createCustomerAppointment = function(data, callback, callbackArguments){  
    	dealership.getDataFromServer(url_appointment_create_update, data, callback, callbackArguments);
    };
    
    this.createCustomerAppointmentCallback = function(data, callbackArguments){
    	window.location = url_appointment+"?flow=create&panel=service&customer_id="+callbackArguments.customer_id+"&appointment_id="+data.id+"&vehicle_id="+callbackArguments.vehicle_id;
    };
    
    //get all the services and repairs 

	/*
    this.getServicesForAppointment = function(ajax_url, panel_id, appt_id)
    {
    	$(document.body).off('click', panel_id+' .servicesdone').on('click', panel_id+' .servicesdone', function(event) {
			var selected = [];
    		$(panel_id+' input:checked').each(function() {
    		    selected.push($(this).attr('value'));
    		});
    		self.saveServicesForAppointment(ajax_url, panel_id, appt_id, selected);				
		}); 

		self.saveServicesForAppointment(ajax_url, panel_id, appt_id,[]);			
    };
    */
   	
    this.getServicesForAppointment = function(appt_id){
		var service_selection  = new ServiceSelection();
		service_selection.panel = "#service-appointment-tab";
		service_selection.pagination_container = "#service-pagination-tab";
		service_selection.search_box = "#dealership_services_search";
		service_selection.service_fetch_url = url_get_all_services;
		service_selection.dealer_code = self.dealer_code;
		service_selection.select_listener = service_selection.selectService;
		service_selection.type = "s";
		service_selection.appointment_id = appt_id;
		service_selection.service_save_url = url_customers_save_appointment_services;	
		service_selection.save_on_select = false;
		
		service_selection.setServices();
		service_selection.after_save_fn = function(){
			self.saveServicesForAppointmentCallback();
		};
		
		  
	 	var repair_selection  = new ServiceSelection();
		repair_selection.panel = "#repair-appointment-tab";
		repair_selection.pagination_container = "#repair-pagination-tab";
		repair_selection.search_box = "#dealership_services_search";
		repair_selection.service_fetch_url = url_get_all_services;
		repair_selection.dealer_code = self.dealer_code;
		repair_selection.select_listener = repair_selection.selectService;
		repair_selection.type = "r";
		repair_selection.appointment_id = appt_id;
		repair_selection.service_save_url = url_customers_save_appointment_services;	
		repair_selection.save_on_select = false;
		
		repair_selection.setServices(); 
		
		$("body").on("click","#servicesdone",function(){
			repair_selection.saveServices();
			service_selection.saveServices();
		});
    };
    
    
    this.saveServicesForAppointment = function(ajax_url, panel_id, appt_id,selected){
    	var data = {'appt_id':appt_id, 'rservice':selected};
    	callbackArguments = {'panel_id': panel_id, 'appt_id':appt_id};
    	dealership.getTemplateFromServer(ajax_url, data, self.getServicesForAppointmentCallback, callbackArguments);
    };    
    
    this.saveServicesForAppointmentCallback = function(data, callbackArguments){
    	//window.location = url_appointment+"?panel=wayaway&appointment_id="+callbackArguments.appt_id;
    	if(self.flow == "create"){
    		window.location = url_appointment+"?flow=create&panel=wayaway&customer_id="+self.cust_id+"&appointment_id="+self.appt_id+"&vehicle_id="+self.vehicle_id;	
    	}    	
    };

    
    this.getWayAwayForAppointment = function(ajax_url, appt_id, panelObject)
    {
    	if(typeof panelObject.dealer_code =="undefined"){
    		panelObject.dealer_code = null
    	}
    	$("body").off('click', panelObject.panel_id+' .wayawaydone').on('click', panelObject.panel_id+' .wayawaydone', function(){
    		
    		var data = {'appt_id':appt_id ,
		  				'wayaway':$(this).attr("rel"), 
		  				'user_id':panelObject.cust_id ,
		  				'dl' : $(".wayaway_form_container.active").find(".wayawaywidget_lisence").val(), 
		  				'company' : $(".wayaway_form_container.active").find(".wayawaywidget_ins_card").val() , 
		  				'card': $(".wayaway_form_container.active").find(".wayawaywidget_ins_card").val() , 
		  				'state': $(".wayaway_form_container.active").find('.waywaywidget_states').find(":selected").val()};
			callbackArguments = {'panel_id': panelObject.panel_id,"el":$(this)};
			dealership.getDataFromServer(url_appointment_wayaway_save , data , panelObject.callback, callbackArguments);
			$(panelObject.panel_id+" .wayawaysuccess").html("");
    		$(panelObject.panel_id+" .wayawaysuccess").hide();
		});	
    	
	$("body").off('click', panelObject.panel_id+' .reserve-wayaway').on('click', panelObject.panel_id+' .reserve-wayaway', function(){
    		
    		var data = {'appt_id':appt_id ,
		  				'wayaway':$(this).attr("rel"), 
		  				
		  				'user_id':panelObject.cust_id ,
		  				'dl' : $(".wayaway_form_container.active").find(".wayawaywidget_lisence").val(), 
		  				'company' : $(".wayaway_form_container.active").find(".wayawaywidget_ins_company").val() , 
		  				'card': $(".wayaway_form_container.active").find(".wayawaywidget_ins_card").val() , 
		  				'state': $(".wayaway_form_container.active").find('.waywaywidget_states').find(":selected").val(),
		  				"reserve":true
    			};
				callbackArguments = {'panel_id': panelObject.panel_id,
						"el":$(this)};
				if(typeof  panelObject.reservecallback == "undefined"){
					 panelObject.reservecallback =  wayawyreserved;
				}
    			dealership.getDataFromServer(url_appointment_wayaway_save , data , panelObject.reservecallback, callbackArguments);
		
		});	
	
    	function wayawyreserved(appt_id,args,el){
    		
    		var panel_id = args["panel_id"]
    		var el  = args["el"]
    		$(panel_id+" .wayawaysuccess").html("Your "+el.data("name")+" has been successfully reserved");
    		$(panel_id+" .wayawaysuccess").show();
    	}
    	
		$("body").off('click', panelObject.panel_id+' .accountinfo').on('click', panelObject.panel_id+' .accountinfo', function(){
			var data = {'user_id':panelObject.cust_id };
    		dealership.getTemplateFromServer(url_appointment_account_info , data , self.getWayAwayAccoutInfoCallback);
        });		
		
		$("body").off('click', panelObject.panel_id+' .wayaway-btn').on('click', panelObject.panel_id+' .wayaway-btn', 
				function(){
						$(panelObject.panel_id+' .wayawaydone').attr("rel", $(this).attr("rel"));
        		}
		);	
		
		var data = {'appt_id':appt_id,'user_id':panelObject.cust_id,"dealer_code":panelObject.dealer_code};
		callbackArguments = {'panel_id': panelObject.panel_id};
		dealership.getTemplateFromServer(ajax_url , data , self.getWayAwayForAppointmentCallback, callbackArguments);
    };
    
    this.getWayAwayForAppointmentCallback = function(response, callbackArguments){
    	$(callbackArguments.panel_id+" .ajax-content").html(response);
    };
    
    this.saveWayAwayForAppointmentCallback = function(data, callbackArguments){
    			var panel = $(callbackArguments["panel_id"])
    			panel.find(".wayaway-btn button").addClass("wayawaybutton");
    			panel.find(".wayaway-btn button").removeClass("btn-info");
    			panel.find(".wayaway-btn button").addClass("btn-default");
    			panel.find(".wayaway-btn button .glyphicon.glyphicon-ok").remove();
    	    	var selected_wayawy_button = callbackArguments["el"]
    	    	
    	    	selected_wayawy = $(".wayaway-btn[rel="+selected_wayawy_button.attr("rel")+"]");
    	    	selected_wayawy.find("button").prepend("<span class='glyphicon glyphicon-ok'></span>");
    	    	selected_wayawy.find("button").addClass("btn-info");
    	    	selected_wayawy.find("button").removeClass("btn-default");
    	    	selected_wayawy.find("button").removeClass("wayawaybutton");
    	    	
    	    	if(self.flow == "create"){
    				window.location = url_appointment+"?flow=create&panel=time&customer_id="+self.cust_id+"&appointment_id="+self.appt_id+"&vehicle_id="+self.vehicle_id;	
    			} 
    	    	
    };
    
    this.getWayAwayAccoutInfoCallback = function(response){
    	if(response["success"] == false){
    		
    		BootstrapDialog.alert('No data found ');
    	}else{
    		$(".wayaway_form_container.active").find(".wayawaywidget_lisence").val(response["DL"]), 
    		$(".wayaway_form_container.active").find(".wayawaywidget_ins_card").val(response["company"]) , 
    		$(".wayaway_form_container.active").find(".wayawaywidget_ins_card").val(response["card"]) , 
    		$(".wayaway_form_container.active").find('.waywaywidget_states').find(":selected").val(response["state"]);
    	}
    };
    
    //bind events 
    // -- save event
    // -- next and previous event    
    this.getTimeForAppointment = function(ajax_url, appt_id, panelObject, date){
    	self.appt_id = appt_id;   	
    	$(document.body).off('click', panelObject.panel_id+' .start-time').on('click', panelObject.panel_id+' .start-time', function(event) {
			panelObject.callback($(this).attr("rel"),$(this));	
		}); 	
		
		$(document.body).off('click', panelObject.panel_id+' .time-grid-control').on('click', panelObject.panel_id+' .time-grid-control', function(event) {
			self.getTimeForAppointment(ajax_url, appt_id, panelObject, $(this).attr('rel'));	
		}); 					
    	
    	if(date != undefined){
    		current_date = moment(date);  
    	}else{
    		var current_date = moment();
    	} 	    	
    	
    	if(current_date.day() ==0){
    		current_date = moment(current_date).add(1, 'day').startOf('isoweek');
    	}else{
    		current_date = moment(current_date).startOf('isoweek');
    	}
    	    	
    	
    	callbackArguments = {"appt_id":appt_id, "panel_id":panelObject.panel_id, "start_week_date":current_date};
    	self.getCalanderForWeek(ajax_url, current_date, callbackArguments);    	
    };   
    
    //if some different function is required to perform in different module
    this.timeSelectionCallback = function(start_time, el){
    	
    	self.selectedTimeSlot = start_time;  
    	//var data = {'id':self.appt_id, 'start_time':start_time};
		//self.createCustomerAppointment(data,self.confirmAppointment);
		
		if(self.flow == "create")
		{
			data = {'id':self.appt_id, 'start_time':start_time};
			dealership.getTemplateFromServer(url_appointment_book, data, self.bookAppointmentCallback);
		
			/*
			$("#btn_create_appointment").removeClass("disabled"); 	
	    	$(document.body).off('click', '#btn_create_appointment').on('click', '#btn_create_appointment', function(event) {
				self.btnClickCreateAppointment(start_time, el);				
			});
			*/
		}
		else{
			var data = {'id':self.appt_id, 'start_time':start_time};
			self.createCustomerAppointment(data,self.appointmentTimeSaved, el);
		}
    	
    	
    };
    
    //get calander from server to schedule user appointment
    this.getCalanderForWeek = function(ajax_url, start_week_date, callbackArguments){
    	var data = {'appt_id':callbackArguments.appt_id,
    				'date':start_week_date.format('YYYY-MM-DD')};	
    	dealership.getTemplateFromServer(ajax_url, data, self.getTimeForAppointmentCallback, callbackArguments);
    };
    
    //calander template callback
    this.getTimeForAppointmentCallback = function(response, callbackArguments){    	
    	$(callbackArguments.panel_id + " .panel-body").html(response);    	
    	var start_week_date = moment(callbackArguments.start_week_date);
    	var end_date = moment(start_week_date).add(5, 'd');

    	$('#time-grid-prev').attr('rel', moment(start_week_date).subtract(2, 'day').format('YYYY-MM-DD'));
    	$('#time-grid-next').attr('rel', moment(start_week_date).add(7, 'day').format('YYYY-MM-DD'));
    	
    	var title = "Week"+start_week_date.format(' of MMM Do - ')+end_date.format('MMM Do');
    	$(callbackArguments.panel_id+' .week-title').html(title);
    }; 
    
    this.getServicesForAppointmentCallback = function(response, callbackArguments){
    	$(callbackArguments.panel_id+" .panel-body").html(response);
    };
    
    this.btnClickCreateAppointment = function(start_time, el){
    	//self.saveAppointmentTime(start_time);
    	//var data = {'id':self.appt_id, 'start_time':self.selectedTimeSlot};
		//self.createCustomerAppointment(data);	
		data = {'appointment_id':self.appt_id};
		dealership.getTemplateFromServer(url_appointment_book, data, self.bookAppointmentCallback);
    }; 
    
    this.bookAppointmentCallback = function(content, callbackArguments){
    	
    	var panel_id = "#appointment";
		self.switchAccordian(panel_id);  	
    	$('#apointment_confirmation_modal .modal-content').html(content);    	
		$('#apointment_confirmation_modal').modal({backdrop: 'static', keyboard: false});
		
		$(document.body).off('change', '#confirmation_checkbox').on('change', '#confirmation_checkbox', function(event) {
		   if( $(this).is(':checked') ){
		   		//$('#apointment_confirmation_modal').modal('hide');
		   }
		});
		
		
		$('#apointment_confirmation_modal').on('hide.bs.modal', function(e){
		  	if(!($('#confirmation_checkbox').is(':checked'))) {
			   	 e.preventDefault();
			     e.stopImmediatePropagation();
			     return false; 
		   	}
		});
		
		$('#apointment_confirmation_modal').on('hidden.bs.modal', function () {
		    window.location = url_appointment;
		});
					    	
    	
    	//window.location = url_overview + "?book_id="+callbackArguments.appointment_id;
    };
        
    this.saveAppointmentTime = function(start_time,el){
    	//self.selectedTimeSlot = start_time; 
    	var data = {'id':self.appt_id, 'start_time':start_time};
		self.createCustomerAppointment(data,self.appointmentTimeSaved,el);	
	};
    
    this.appointmentTimeSaved = function(content,el){
    	$(".start-time").removeClass("btn-success");
    	$(".start-time").addClass("btn-default");
    	
    	if (typeof el !="undefined"){
//    		console.info(el)
    		el.addClass("btn-success");
    		el.removeClass("btn-default")
    	}
    	if(self.date_save_callback !=null){
    		console.info("calling date save")
    		self.date_save_callback()
    	}
    	
    };
}





