function DealershipCustomer() {
	var self = this;
	var dealership = new Dealership();
	var dealershipOverview = new DealershipOverview();
	var dealershipAppointment = new DealershipAppointment();
	
	this.dealer_code;
	
	this.setEventListeners = function(){
		
		$(document.body).on('submit', '.customer-page #searchcust_form', function(event) {
		    event.preventDefault();
		    var data = $(this).serializeArray();
		    dealershipOverview.overviewTimeDailySearch(data[0].value, data[1].value);
       		return false;
		}); 
		
		$(document.body).off('click', '.newcustomer .edit-advisor').on('click', '.newcustomer .edit-advisor', function(event) {
			//self.selected_vehicle = $(this);
			var advisor_selection = new AdvisorSelection();
			advisor_selection.panel = "#advisor-appointment";
			advisor_selection.dealer_code = self.dealer_code;
			advisor_selection.pagination_container = "#advisor_pagination";
			advisor_selection.select_listener = self.selectAdvisor;
			advisor_selection.advisor_fetch_url = url_get_all_advisors_ajax;
			advisor_selection.advisor_save_url = url_save_advisor_ajax;
			advisor_selection.setAdvisors();			
		}); 
		
		$(document.body).on('click', '.customer-list-row', function(event) {	
			var cust_id = $(this).attr("rel");
			var panel_id = "#customer-list-detail-"+cust_id;		
	        dealershipAppointment.getCustomerForAppointment(panel_id, cust_id, self.dealer_code);		
		}); 
		
		/*
		$(document.body).on('change', '.customer-notes', function(event) {
			$("input[name=customer_notes]").val($(this).val());
		});	
		*/	
		
		$(document.body).on('click', '.add-cust-submit', function(event) {
			if($('#form-save-customer').hasClass("pending")){
				$('#form-save-customer-submit').click();	
			}else if($('#form-save-vehicle').hasClass("pending")){
				$('#form-save-vehicle-submit').click();
			}else if($('#form-save-appointment').hasClass("pending")){
				$('#form-save-appointment-submit').click();
			}else if($('#form-save-reminder').hasClass("pending")){
				$('#form-save-reminder-submit').click();
			}
			else{
				self.enableAppointment();
			}				
		}); 
		
		$(document.body).on('click', '.btn-schedule-apt', function(event) {
			window.location = url_appointment+"?flow=create&panel=service&customer_id="+$(this).attr("customer_id")+"&vehicle_id="+$(this).attr("vehicle_id")+"&appointment_id="+$(this).attr("appointment_id");
		});
		
		
		
		$(document.body).on('submit', '#form-save-customer', function(event) {
			event.preventDefault();
			$('.add-cust-submit').addClass("disabled");
		    var data = $(this).serializeArray();
		    callbackArguments = {'panel_id':'#form-save-customer', 'next':'#form-save-vehicle-submit'};
		    dealership.getDataFromServer(url_customers_add_user, data, self.saveCustomerCallback, callbackArguments);
       		return false;		
		});
		
		
		$(document.body).on('submit', '#form-save-vehicle', function(event) {
			event.preventDefault();
			$('.add-cust-submit').addClass("disabled");
		    var data = $(this).serializeArray();
		    callbackArguments = {'panel_id':'#form-save-vehicle', 'next':'#form-save-appointment-submit'};
		    dealership.getDataFromServer(url_customers_add_vehicle, data, self.saveVehicleCallback, callbackArguments);
       		return false;		
		}); 
		
		$(document.body).on('submit', '#form-save-appointment', function(event) {
			event.preventDefault();
			$('.add-cust-submit').addClass("disabled");
		    var data = $(this).serializeArray();
		    callbackArguments = {'panel_id':'#form-save-appointment', 'next':'#form-save-reminder-submit'};
		    dealership.getDataFromServer(url_customers_add_appointment, data, self.saveAppointmentCallback, callbackArguments);
       		return false;		
		}); 
		
		$(document.body).on('change', '.chk-reminder', function(event) {
			$('.chk-reminder-options').toggle();
			if($('#form-save-reminder').hasClass("pending")){
				$('#form-save-reminder').removeClass("pending");
			}else {
				$('#form-save-reminder').addClass("pending");
			}
		});
		
		$(document.body).on('submit', '#form-save-reminder', function(event) {
			event.preventDefault();
			$('.add-cust-submit').addClass("disabled");
		    var data = $(this).serializeArray();
		    callbackArguments = {};
		    dealership.getDataFromServer(url_customers_add_reminder, data, self.enableAppointment, callbackArguments);
       		return false;		
		}); 
		
		/*
		$(document.body).on('click', '.fa', function(event) {
			if($(this).hasClass('fa-plus-circle')){
				$(this).removeClass('fa-plus-circle');
				$(this).addClass('fa-minus-circle');
			}
			else{
				$(this).removeClass('fa-minus-circle');
				$(this).addClass('fa-plus-circle');
			}
		});
		*/
	};
	
	this.getVehicleWidget = function(vehicles_data){
		var vehicle_add_widget = new VehicleWidget();
		vehicle_add_widget.vehicles = vehicles_data;
		vehicle_add_widget.vin_text_input = $("#vin_vehicle");
		vehicle_add_widget.dropdownobj = ".vehichle_selectbox";
		
		vehicle_add_widget.attachVehicleFound(self.setVehicleId);
		
		vehicle_add_widget.initialize();
	};
	
	this.setVehicleId = function(vehicles){
		if (Object.keys(vehicles).length == 1){
			var vehichle_id_control = $("#vehicle_id_field");
			$.each(vehicles,function(k,v){
				vehichle_id_control.val(vehicles[k]["id"]);
			});					
		}
	};
	
	this.saveCustomerCallback = function(data, callbackArguments){
		self.generalFromSettings();
		if(data.status == "success"){
			$(callbackArguments.panel_id).removeClass("pending");
			$('.btn-schedule-apt').attr("customer_id", data.id);
			//$('#user_id_vehicle').val(data.id);
			//$('#customer_id_appt').val(data.id);
			$('.customer_id_hidden').val(data.id);
			self.updateProgress(33);
			$(callbackArguments.next).click();	
					
		}
		else{			
			self.setFormErrors(data.errors);
		}
	};
	
	this.saveVehicleCallback = function(data, callbackArguments){
		self.generalFromSettings();
		if(data.status == "success"){
			$(callbackArguments.panel_id).removeClass("pending");
			$('.btn-schedule-apt').attr("vehicle_id", data.id);
			$('#vehicle_id_appt').val(data.id);
			self.updateProgress(66);
			$(callbackArguments.next).click();		
		}
		else{
			self.setFormErrors(data.errors);
		}
	};
	
	this.saveAppointmentCallback = function(data, callbackArguments){
		self.generalFromSettings();
		if(data.status == "success"){
			$(callbackArguments.panel_id).removeClass("pending");
			$('.btn-schedule-apt').attr("appointment_id", data.id);
			$('#vehicle_id_appt').val(data.id);
			self.updateProgress(100);
			if($('.chk-reminder').attr("checked")){
				$(callbackArguments.next).click();
			}else{
				self.enableAppointment();
			}
					
		}
		else{
			self.setFormErrors(data.errors);
		}
	};
	
	this.generalFromSettings = function(){
		$('.newcustomer .error').addClass("hidden");
		$('.newcustomer .error .details').html("");
		$('.add-cust-submit').removeClass("disabled");
	};
	
	this.updateProgress = function(value){
		$('.progress-bar').css('width', value+'%').attr('aria-valuenow', value).html(value+' %'); 
	};
	
	this.enableAppointment = function(){	
		self.updateProgress(100);
		$('.add-cust-submit').addClass("disabled");	
		$('.btn-schedule-apt').removeClass("disabled");
	};
	
	this.setFormErrors = function(errors){	
		$('.newcustomer .error').removeClass("hidden");	
		$.each( errors, function( key, value ) {
	 		$('.newcustomer .error .details').append("<div>"+key+":"+value+"</div>");
		});
	};

	
	//open the customer detaial according to selected customer
	this.switchCustomer = function(id)
	{		
		var element = '#customer-list-detail-'+id;
		if($(element).hasClass('hidden'))
		{
			$(element).removeClass('hidden');
		}
		else{ $(element).addClass('hidden'); }		
	};
	
	this.selectAdvisor = function(advisor,dont_save){
		
		//$('.newcustomer .media img')
		$('.newcustomer .advisor-panel p').html("Advisor: <br>"+advisor.find(".advisor_name").html());
		$('.newcustomer #advisor_id_appt').val(advisor.find(".advisor__id").val());

		$('#select-advisor-modal').modal('hide');
	};
	

}