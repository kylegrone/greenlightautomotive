function DealershipOverview(){
	dealership = new Dealership();
	var self = this;
	var firstTimerInterval = null;
	var scrollTimerInterval = null;
	var shopOpenTime;
	var shopCloseTime;
	var timeSlot;
	
	this.dealer_code;
	this.search;
	this.criteria;
	this.cust_id;
	this.appt_id;
	this.tmp_slab_date = [];
	this.totalSlabCalls = 0;
	this.totalSlabCallsReturned = 0;
	
	this.filters;
	
	//set the appointment filters either it daily, weekly, time , advisor , status or search
	this.setEventListeners = function(){
        $(document.body).on('click', '.save-appointment-detail', function(event) {
            var id = $(this).attr("rel");
            $('#apt-credit-form-submit-'+id).click();
            $('#apt-vehicle-form-submit-'+id).click();
            $('#apt-insurance-form-submit-'+id).click();
        });
        
        
        $(document.body).on('submit', '.apt-detail-form', function(event) {
			event.preventDefault();
		    var data = $(this).serializeArray();
		    var callbackArguments = {'panel_id':"#"+$(this).attr("id")};
            var url = $(this).attr("action")
		    dealership.getDataFromServer(url, data, self.appointmentDetailUpdateCallback, callbackArguments);
       		return false;		
		}); 
        
        
                
                
		/*
		$('.input-group.date').datepicker({
			format: 'DD M dd, yyyy',
			todayHighlight: true,
		}).on('hide', function(e) {
	        self.setOverviewFilters();
	    }); 
	    */  
	    
	    $('.filter-date-picker').datepicker({
	    	todayHighlight: true,
	    }).on('changeDate', function(e){	    	
	    	self.setOverviewFilters($('.filter-date-picker').datepicker('getDate'));
	    	$('.filter-date-picker').datepicker('hide');
	    });
	    
	    /*
	    $('.input-group.date').datepicker({
			format: 'DD M dd, yyyy',
			todayHighlight: true,
		}).on('hide', function(e) {
	        self.setOverviewFilters();
	    }); 
	    */
		

		$(document.body).on('submit', '.overview-page #searchcust_form', function(event) {
		    event.preventDefault();
		    var data = $(this).serializeArray();
		    self.overviewTimeDailySearch(data[0].value, data[1].value);
       		return false;
		}); 
		
		
		$(document.body).on('click', '#new-appointment-btn', function(event) {
			$("#customer-search").removeClass("collapse").addClass("in");
		}); 
		
		$(document.body).on('click', '.appointment_row .customer', function(event) {				
		    self.showAppointmentDetail($(this).attr('vehicle_id'), $(this).attr('customer_id'), $(this).attr('rel'));
		});  
		
		
		$(document.body).on('click', '.main_filter .btn', function(event) {
			self.setOverviewFilters($('.filter-date-picker').datepicker('getDate'), '.main_filter', this);				
		});  
		
		$(document.body).on('click', '.sub_filter .btn', function(event) {
			self.setOverviewFilters($('.filter-date-picker').datepicker('getDate'), '.sub_filter', this);				
		});  			
			
		$(document.body).on('mouseover', '.dd_status_title', function(event) {
			//$(this).closest('.dropdown').append("<div></div>");		
			$(this).siblings().html($("#dd_status_menu").html());				
		});  
		
		$(document.body).on('mouseover', '.dd_wayaway_title', function(event) {	
			$(this).siblings().html($("#dd_wayaway_menu").html());				
		}); 
		
		$(document.body).on('click', '.dd_advisor_title', function(event) {	
			data = {'datetime':$(this).attr("time")};
			callbackArguments = {'panel_id': $(this).siblings()};
			dealership.getDataFromServer(url_ov_advisor, data, self.getAvlAdvisorListCallback, callbackArguments);
				
		}); 
		
		  
		
		$(document.body).on('click', '.dropdown-change-apt a', function(event) {
			$(this).changeAppointment();			
		});	
		
		$(document.body).off('click',' .filter-date-control').on('click',' .filter-date-control', function(event) {
			var date_string = $(this).attr('rel');
			
			
			//$('.filter-date-picker').datepicker('update', new Date(date_string));
			//jQuery.noConflict(); 
			//$('.filter-date-picker').datepicker('setDate', new Date(date_string)).datepicker('update');
			//$('.filter-date-picker').datepicker('update', new Date(date_string))
			
			$('.filter-date-picker').data({date: new Date(date_string)});
			$('.filter-date-picker').datepicker('update');
			$('.filter-date-picker').datepicker().children('input').val(date_string);
//			self.setOverviewFilters(moment(date_string));	
		});
		
		$(document.body).off('click', '.time-carryover, .time-adjust').on('click', '.time-carryover, .time-adjust', function(event) {			
			var apptTime = moment($(this).attr("datetime"));		
			self.fillCarryOver(apptTime);	
			$('.carryover-date-picker').datepicker({
    			todayHighlight: true,
		    }).on('changeDate', function(e){	  
		    	self.fillCarryOver($('.carryover-date-picker').datepicker('getDate'));  	
			});
			$('.carryover-date-picker').datepicker('setDate', new Date()).datepicker('update');	
			
			$('#form-carryover-time #appointment_id').attr("value", $(this).attr("rel"));
			
			$('#form-carryover-time #appt_actual_time').html(apptTime.format("DD/MM/YYYY hh:mm A"));
			
			
			
			$('#time-carryover-modal').modal('show');			
			$('#time-carryover-modal').off('hidden.bs.modal').on('hidden.bs.modal', function () {
			    
			});
		});	
		
		$(document.body).off('click', '.carryover-date-control').on('click', '.carryover-date-control', function(event) {			
			self.selectCarryOver(parseInt($(this).attr("rel")));
		});
		
		
		$(document.body).on('submit', '#form-carryover-time', function(event) {
		    event.preventDefault();
		    var data = $(this).serializeArray();		    
		    //var data = {'id':self.appt_id, 'start_time':start_time};
			dealership.getDataFromServer(url_appointment_create_update, data, self.carryOverCallback);
       		return false;
		}); 
		
		$(document.body).on('click', '.HeadRow', function(event) {		
			$(this).next().slideToggle();
            $(this).find(".glyphicon-chevron-down").toggleClass("hide");
            $(this).find(".glyphicon-chevron-up").toggleClass("hide");
		});
        
        
        $(document.body).on('click', '.remove-apt-service', function(event) {	
            self.removeService($(this));
		});
        
					
	};
	
	this.carryOverCallback = function(data, callbackArguments){
		$('#time-carryover-modal').modal('hide');
		$('#time-carryover-confirmation-modal').modal('show');		
	};
	
    this.appointmentDetailUpdateCallback = function(data, callbackArguments)
    {
        if(data['status'] == "error"){
            $(callbackArguments.panel_id + " .alert-success").addClass("hidden");
            $(callbackArguments.panel_id + " .alert-danger").removeClass("hidden");
            $(callbackArguments.panel_id + " .alert-danger .details").html(data['message']);
        }
        else{
            $(callbackArguments.panel_id + " .alert-danger").addClass("hidden")
            $(callbackArguments.panel_id + " .alert-success").removeClass("hidden");
            $(callbackArguments.panel_id + " .alert-success .details").html(data['message']);
        }
    };
    
	this.fillCarryOver = function(date){
		var apptTime = moment(date);
		var currentTime = moment();
		if(apptTime.isBefore(currentTime)){
			var difference = currentTime - apptTime;
		}
		
		
		var data = {'date':apptTime.format('YYYY-MM-DD'), 'dealer_code':self.dealer_code};
		var callbackArguments = {'date': apptTime} ;
		//var data = {'dealer_code':self.dealer_code};
		//var url = get_available_slabs_for_date+"?date="+currentTime.format('YYYY-MM-DD')+"&dealer_code="+self.dealer_code;
		dealership.getGetDataFromServer(get_available_slabs_for_date, data, self.getAvlSlabListCallback, callbackArguments);
		
		
	};

	this.getAvlSlabListCallback = function(data, callbackArguments)
	{		
		
		self.tmp_slab_date = data['slabs'];
		console.info(self.tmp_slab_date);
		//var date = moment(callbackArguments.date);
		//$('#carryover-date-text').html(date.format('dddd MMM DD, YYYY'));
		var len = data['slabs'].length;
		if(len != 0){
			$('#carryover-date-text').attr("rel",len-1);
			self.selectCarryOver(0);
		}	
	};
	
	this.selectCarryOver = function(index){
		$('#carryover-date-text').html(self.tmp_slab_date[index]["name"]);
		$('#carryover-date-text').attr("value", self.tmp_slab_date[index]["value"]);
		var length = parseInt($('#carryover-date-text').attr("rel"));
		if(index == 0){
			$('#carryover-date-prev').attr('rel', length);
		}
		else{
			$('#carryover-date-prev').attr('rel',index-1);
		}
		
		if(index == length){
			$('#carryover-date-next').attr('rel', 0);
		}
		else{
			$('#carryover-date-next').attr('rel', index+1);
		}	
	};
		
	this.setOverviewFilters = function(selected_date, filter, current){
				
		//var selected_date = $('.filter-date-control').datepicker('getDate');
		
		var date = moment();
		
		if ( selected_date != undefined){
			
			date = moment(selected_date);
		}	
		
		if(filter !== undefined)
		{
			$(filter+' .btn').removeClass('btn-info');
		    $(filter+' .btn').addClass('btn-default');
		    $(current).removeClass('btn-default');
		    $(current).addClass('btn-info');
		    $(filter).attr('rel', $(current).attr('rel'));	  
		}
		
		if($('.sub_filter').attr('rel') == "weekly"){
			date = moment(date).startOf('isoweek');
			$('#filter-date-text').html('Week of '+date.format('MMM DD, YYYY'));
			$('#filter-date-prev').attr('rel', moment(date).subtract(2, 'day').format('YYYY-MM-DD'));
	    	$('#filter-date-next').attr('rel', moment(date).add(7, 'day').format('YYYY-MM-DD'));
		}
		else
		{
			
			$('#filter-date-text').html(date.format('dddd MMM DD, YYYY'));
			$('#filter-date-prev').attr('rel', moment(date).subtract(1, 'day').format('YYYY-MM-DD'));
    		$('#filter-date-next').attr('rel', moment(date).add(1, 'day').format('YYYY-MM-DD'));
		}
		  
	    //url = "../"+"overview/"+$('.main_filter').attr('rel')+"/"+$('.sub_filter').attr('rel');
	    url = "../"+"overview/"+$('.sub_filter').attr('rel')+"?date="+date.format('YYYY-MM-DD HH:mm')+"&q="+$('.main_filter').attr('rel');
	    var content = $('.main_filter').attr('rel')+"_"+$('.sub_filter').attr('rel');
	    self.filters = content;
	    $("#loading_page").show();
		$.ajax({
            url: url,
            type: "get",
            error:function(){
            	$("#loading_page").hide();
            },
            success: function(response) {            	
            	$("#loading_page").hide();
            	var result =  $($.parseHTML(response)).filter("#ajax_main_content"); 
            	var breadcrumb =  $($.parseHTML(response)).filter(".breadcrumb-top"); 
            	
            	//alert($($.parseHTML(response)).filter(".open-time")[0].innerHTML);
            	if($($.parseHTML(response)).filter(".open-time")[0].innerHTML == ""){
            		self.shopOpenTime = null;
            		self.shopCloseTime = null;
            	}else{
            		self.shopOpenTime = moment($($.parseHTML(response)).filter(".open-time")[0].innerHTML);
					self.shopCloseTime = moment($($.parseHTML(response)).filter(".close-time")[0].innerHTML);
					self.timeSlot = $($.parseHTML(response)).filter(".slot-duration")[0].innerHTML;
            	}
            	
				console.info(self.shopOpenTime);
				console.info(self.shopCloseTime);
                $('#main_content').html(result[0].innerHTML);
                $('.breadcrumb-top').html(breadcrumb[0].innerHTML);
				switch(content) {
				    case "time_daily":
				    	if(self.appt_id != ""){ 
				    		//alert(self.appt_id);
				    		self.overviewTimeDailyApptSearchDetail(self.appt_id, '#overview_time_daily'); 
				    	}else { 
				    		self.overviewTimeDaily('#overview_time_daily'); 
				    	}				        
				        break;
				    case "time_weekly":
				        //self.overviewTimeWeekly();
				        self.overview("time", "weekly");
				        break;
				   	case "advisor_daily":
				        self.overview("advisor", "daily");
				        break;
				  	case "advisor_weekly":
				        self.overview("advisor", "weekly");
				        break;
				    case "status_daily":
				    	$('.GridRow').remove();
				        self.overview("status", "daily");
				        break;
				    case "status_weekly":
				        self.overview("status", "weekly");
				        break;
				    default:
				        break;
				}
            }
        });					
	};
	
	this.updateWallboard = function(obj)
	{
		var new_data = eval("(" + obj['data']["new_data"] + ')');
		var old_data = eval("(" + obj['data']["old_data"] + ')');
		if(old_data[0]["fields"]["appointment_status"] != new_data[0]["fields"]["appointment_status"])
		{	  
			self.getWallboardData();
		}
	};
	
	this.getWallboardData = function()
	{
		var data = {"date":moment().format("YYYY-MM-DD")};
		dealership.getTemplateFromServer(url_ov_time_wallboard, data, self.updateWallboardCallback);
	};
	
	this.updateWallboardCallback = function(content, callbackArguments)
	{
		$(".da_menu").html(content);
	};
	
	this.setupRealTimeUpdates = function(obj)
	{
		if(obj["data"] != null){
			var new_data = eval("(" + obj['data']["new_data"] + ')');
			var old_data = eval("(" + obj['data']["old_data"] + ')');
			console.info(old_data);
			
			switch(self.filters) {
			    case "time_daily":
			    	self.realUpdateTime("daily", old_data, new_data);			        
			        break;
			    case "time_weekly":
			        self.realUpdateTime("weekly", old_data, new_data);
			        break;
			   	case "advisor_daily":
			        self.realUpdate("advisor", "advisor","daily", old_data, new_data);
			        break;
			  	case "advisor_weekly":
			        self.realUpdate("advisor", "advisor", "weekly", old_data, new_data);
			        break;
			    case "status_daily":
			    	console.info("check pass");
			        self.realUpdate("status", "appointment_status", "daily", old_data, new_data);
			        break;
			    case "status_weekly":
			        self.realUpdate("status", "appointment_status", "weekly", old_data, new_data);
			        break;
			    default:
			        break;
			}			 
		}
		console.info(obj);
	};
	
	
	this.realUpdateTime = function(type, old_data, new_data)
	{
		var old_date = moment(old_data[0]["fields"]["start_time"], "YYYY-MM-DD[T]HH:mm:ss[Z]");
		var old_slab_id = old_date.format("[#time_"+type+"_slab_]YYYY_MM_DD_HH_mm");
		if($(old_slab_id).length) {
			if(type== "daily"){
				self.getTimeDailySlab(null, old_date, old_slab_id);
			}
			else{
				self.getTimeWeeklyAppointmentSlab(old_date, old_slab_id);
			}
			 
		}
		
		var new_date = moment(new_data[0]["fields"]["start_time"], "YYYY-MM-DD[T]HH:mm:ss[Z]");
		var new_slab_id = new_date.format("[#time_"+type+"_slab_]YYYY_MM_DD_HH_mm");			
		if($(new_slab_id).length && new_slab_id != old_slab_id) 
		{
			if(type== "daily"){
				self.getTimeDailySlab(null, new_date, new_slab_id);
			}
			else{
				self.getTimeWeeklyAppointmentSlab(new_date, old_slab_id);
			}
			 
		}
	};
	
	
	this.realUpdate = function(type, column, period, old_data, new_data)
	{
		if(period == "daily"){
			if(type == "advisor"){ var slabs_data_url = url_ov_advisor_daily_slab;}
			else if (type == "status") {var slabs_data_url = url_ov_status_daily_slab;}
		}
		else{
			if(type == "advisor"){var slabs_data_url = url_ov_advisor_weekly_slab;}
			else if (type == "status")  {var slabs_data_url = url_ov_status_weekly_slab;}
		}
		
		
		var old_id = old_data[0]["fields"][column];
		var old_date = moment(old_data[0]["fields"]["start_time"], "YYYY-MM-DD[T]HH:mm:ss[Z]");			
		if(period == "daily"){
			
			var old_slab_id = "#"+period+"_slab_"+old_id;
			if($(old_slab_id).length) {				
				self.getDailySlabContent(slabs_data_url, old_date, old_id, true);				
			}
		}
		else{
			var old_slab_id = "#weekly_slab_"+old_date.format("YYYY_MM_DD_")+old_id;
			if($(old_slab_id).length) {	
				self.getWeeklyAppointmentSlab(old_slab_id, old_date, old_id, slabs_data_url);
			}
		}
		
		
		
		var new_id = new_data[0]["fields"][column];
		var new_date = moment(new_data[0]["fields"]["start_time"], "YYYY-MM-DD[T]HH:mm:ss[Z]");
		if(period == "daily"){
			var new_slab_id = "#"+period+"_slab_"+new_id;
			if($(new_slab_id).length && new_slab_id != old_slab_id){
				self.getDailySlabContent(slabs_data_url, new_date, new_id, true); 			
			}
		}
		else{
			var new_slab_id = "#weekly_slab_"+new_date.format("YYYY_MM_DD_")+new_id;
			if($(new_slab_id).length && new_slab_id != old_slab_id){
				self.getWeeklyAppointmentSlab(new_slab_id, new_date, new_id, slabs_data_url);
			}
		}
	};
	
	//populate all the appointment slabs of given date
	this.overviewTimeDaily = function(panel_id, template, advisor_id){	
		//var date = moment();
		//var slab = moment({ y:date.format('YYYY'), M:date.format('M')-1, d:date.format('D'), h:07, m :00}); 
		if(self.shopOpenTime != null){
			var slab = self.shopOpenTime;
			current_slab = self.getCurrentSlabForScroll('#time_daily_slab');
			self.totalSlabCalls = 0;
			self.totalSlabCallsReturned = 0;
			while(slab.isBefore(self.shopCloseTime))
			{
				self.totalSlabCalls = self.totalSlabCalls + 1;
				self.getTimeDailySlab(panel_id, slab, current_slab, template, advisor_id);  
				slab = moment(slab).add(self.timeSlot, 'm');
				//slab = new Date(start.getTime() + slot*60000);			    	
			}
		}
	};
	
	this.getTimeDailyAllSlabs = function()
	{
		
	};
	
	//get the template of individual slab
	this.getTimeDailySlab = function(panel_id, date, current_slab, template, advisor_id)
	{	
		var slabid = "time_daily_slab_"+date.format('YYYY_MM_DD_HH_mm');
		//$(panel_id).append('<table class="table table-striped table-headgray mb-0 daily_view_table"><tbody id="'+slabid+'"></tbody></table>');
		$(panel_id).append('<div id="'+slabid+'" class="GridRow daily_view_table" >');
		data = {'datetime':date.format('YYYY-MM-DD HH:mm'), 'template':template, 'advisor_id':advisor_id};
		callbackArguments = {'panel_id': panel_id, 'slab_id': '#'+slabid, 'current_slab':current_slab};
		dealership.getTemplateFromServer(url_ov_time_daily_slab, data, self.getTimeDailySlabCallback, callbackArguments);
	};
	
	this.getTimeDailySlabCallback = function(response, callbackArguments)
	{	
		$(callbackArguments.slab_id).html(response);	
		self.scroll('#time_daily_slab', callbackArguments);	
	};
	
	
	this.overviewTimeDailyApptSearchDetail = function(appt_id, panel_id)
	{		        
        var data = {'appt_id':appt_id};
        callbackArguments = {'panel_id': panel_id};
		dealership.getTemplateFromServer(url_ov_time_daily_search_appt, data, self.overviewTimeDailyApptSearchDetailCallback, callbackArguments);
	};
	
	this.overviewTimeDailyApptSearchDetailCallback = function(response, callbackArguments)
	{
		$(callbackArguments.panel_id).append(response);
		$(callbackArguments.panel_id +" .HeadRow").click();
		$(callbackArguments.panel_id +" .customer").click();
		
	};
	
	this.overviewTimeDailySearch = function(search, criteria)
	{		
		var date = moment();
		var data = {'date':date.format('YYYY-MM-DD'), 'search':search, "criteria":criteria};
		dealership.getDataFromServer(url_ov_time_daily_search, data, self.overviewTimeDailySearchCallback);
	};
	
	this.overviewTimeDailySearchCallback = function(data, callbackArguments)
	{
		if(data.type == "error"){
			$('.cust-search-error .text_red').removeClass("hidden");
		}else{
			window.location = data.url;
		}
	};
	
		
	this.overviewTimeWeekly = function(type){
		var next = moment(self.shopOpenTime).startOf('isoweek');	
		current_slab = self.getCurrentSlabForScroll('time_weekly_slab');
		//loop over days of week first
		for(loopday=0; loopday<6; loopday++){			
			self.getWeeklyAppointmentDay(next, current_slab, type);	
			next = moment(next).add(1, 'day');		
		}		
	};
	
	this.getWeeklyAppointmentDay = function(date, current_slab, type, slabs_from_db){		
			
		var id = type+"_weekly_day_"+date.format('YYYY_MM_DD');		
		var data = {'date':date.format('YYYY-MM-DD'), 'id':id, 'type':type};
		if(type == "advisor" || type == "status"){
			var callbackArguments = {'id':'#'+id, 'date':date, 'current_slab':current_slab, 'type':type, 'slabs_from_db':slabs_from_db};
			dealership.getTemplateFromServer(url_ov_time_weekly_day, data, self.fillWeeklyAppointmentDay, callbackArguments);
		}else{
			var callbackArguments = {'id':'#'+id, 'date':date, 'current_slab':current_slab};
			dealership.getTemplateFromServer(url_ov_time_weekly_day, data, self.fillTimeWeeklyAppointmentDay, callbackArguments);
		}		
	};
	
	this.fillWeeklyAppointmentDay = function(response, callbackArguments)
	{		
		$('#overview_time_weekly #'+callbackArguments.date.format('dddd')).html(response);
		/*	
		if(callbackArguments.type == "advisor"){var url = url_ov_advisor_weekly_slab;}
		else {var url = url_ov_status_weekly_slab;}
		for (i in callbackArguments.slabs_from_db['data'])
		{			
			var slab_id = callbackArguments.type+"_weekly_slab"+callbackArguments.date.format('_YYYY_M_D_')+callbackArguments.slabs_from_db['data'][i]['id'];
			$(callbackArguments.id).append("<div class='panel panel-default' id='{0}'><div class'slabs_loader'><img src='../../static/images/loader.png'/></div></div>".replace('{0}', slab_id));	
			self.getWeeklyAppointmentSlab("#"+slab_id, callbackArguments.date, callbackArguments.slabs_from_db['data'][i]['id'], callbackArguments.slabs_from_db['data'][i]['title'], url);  
		}
		*/
	};
	
	this.getWeeklyAppointmentSlab = function(slab_id, date, id, url)
	{
		var data = {'date':date.format('YYYY-MM-DD'), 'id':id};
		var callbackArguments = {'slab_id':slab_id};
		dealership.getTemplateFromServer(url, data, self.getWeeklyAppointmentSlabCallback, callbackArguments);
	};
	
	this.getWeeklyAppointmentSlabCallback = function(response, callbackArguments)
	{
		$(callbackArguments.slab_id).html(response);				
	};
	
		
	this.fillTimeWeeklyAppointmentDay = function(response, callbackArguments)
	{		
		$('#overview_time_weekly #'+callbackArguments.date.format('dddd')).html(response);	
		
		/*	
		var slab = moment({ y:callbackArguments.date.format('YYYY'), M:callbackArguments.date.format('M')-1, d:callbackArguments.date.format('D'), h:07, m :00}); 
		total = 61;
		for(slot=1; slot <= total; slot++)
		{			
			var slab_id = "time_weekly_slab_"+slab.format('YYYY')+"_"+slab.format('M')+"_"+slab.format('D')+"_"+slab.format('HH')+"_"+slab.format('mm');
			$(callbackArguments.id).append("<div class='panel panel-default' id='{0}'><div class'slabs_loader'><img src='../../static/images/loader.png'/></div></div>".replace('{0}', slab_id));	
			self.getTimeWeeklyAppointmentSlab(slab_id, slab, callbackArguments.current_slab);  
			slab = moment(slab).add(10, 'm');	
		}
		*/
	};
	
	this.getTimeWeeklyAppointmentSlab = function(date, current_slab)
	{
		var slab_id = date.format('[time_weekly_slab_]YYYY_MM_DD_HH_mm');
		var data = {'datetime':date.format('YYYY-MM-DD HH:mm'), 
					"id":slab_id};
		var callbackArguments = {'slab_id':'#'+slab_id, 'current_slab':current_slab, 'day':"#"+date.format('dddd')};
		dealership.getTemplateFromServer(url_ov_time_weekly_slab, data, self.getTimeWeeklyAppointmentSlabCallback, callbackArguments);	 
	};		
	
	this.getTimeWeeklyAppointmentSlabCallback = function(response, callbackArguments)
	{
		$(callbackArguments.slab_id).html(response);	
		//scroll('time_weekly_slab', slab_id, current_slab, 366, day);		
	};
	
	
	this.overview = function(type, duration){
		var slabs_url;
		var slabs_data_url;
		if(type == "advisor"){ slabs_url = url_ov_advisor; slabs_data_url = url_ov_advisor_daily_slab;}
		else if (type == "status") {slabs_url = url_ov_status; slabs_data_url = url_ov_status_daily_slab;}
		data = {};
		if(duration == "weekly"){
			self.overviewTimeWeekly(type);
			//var callbackArguments = {'date':self.shopOpenTime, 'type':type};
			//dealership.getTemplateFromServer(slabs_url, data, self.overviewWeeklyCallback, callbackArguments);
		}else{
			var callbackArguments = {'date':self.shopOpenTime, 'slabs_data_url':slabs_data_url};
			dealership.getDataFromServer(slabs_url, data, self.overviewDailyCallback, callbackArguments);
			
		}
	};
	
	/*
	this.overviewWeeklyCallback = function(data, callbackArguments){
		var next = moment(callbackArguments.date).startOf('isoweek');	
		var date = moment(callbackArguments.date);
		var day = '#'+date.format('dddd');
		current_slab = self.getCurrentSlabForScroll('time_weekly_slab');
		//loop over days of week first
		for(loopday=0; loopday<6; loopday++){			
			self.getWeeklyAppointmentDay(next, current_slab, callbackArguments.type, data);	
			next = moment(next).add(1, 'day');		
		}
		$("#overview_time_weekly").scrollLeft($(day).offset().left);
	};
	*/
	
	this.overviewDailyCallback = function(data, callbackArguments){
	    self.createDailySlab(callbackArguments.date, data, callbackArguments.slabs_data_url);
	};
		
		
		
	this.createDailySlab = function(date, slabs_from_db, url)
	{		
		if(self.shopOpenTime != null){
			for (i in slabs_from_db['data'])
			{
				self.getDailySlabContent(url, date, slabs_from_db['data'][i]['id'], false);
			}
		}			
	};
	
	this.getDailySlabContent = function(url, date, id, open)
	{
		var slabid = "daily_slab_"+id;
	  	//$('#overview_time_daily').append('<table class="table table-striped table-headgray mb-0 daily_view_table"><tbody id="'+slabid+'"></tbody></table>');
		
		$('#overview_time_daily').append('<div id="'+slabid+'" class="GridRow daily_view_table" >');
		var data = {'date':date.format('YYYY-MM-DD'), 'id':id};
		var callbackArguments = {'slabid':'#'+slabid, "open":open};
		dealership.getTemplateFromServer(url, data, self.createDailySlabCallback, callbackArguments);
	};
	
		
	this.createDailySlabCallback = function(response, callbackArguments)
	{
		$(callbackArguments.slabid).html(response);
		if(callbackArguments.open == true){
			$(callbackArguments.slabid+" .HeadRow").click();
		}
	};
	
	
	this.showAppointmentDetail = function(vehicle_id, customer_id, appointment_id, checkin, appt_status)
	{
		var element = '#appointment_detail_'+appointment_id;
		if($(element).hasClass('hidden'))
		{
			self.refreshAppointmentDetail(vehicle_id, customer_id, appointment_id, checkin,appt_status);
			$(element).removeClass('hidden');
		}
		else{ $(element).addClass('hidden'); }		 		
	};
	
	this.refreshAppointmentDetail = function(vehicle_id, customer_id, appointment_id, checkin,appt_status)
	{
		var data = {'vehicle_id':vehicle_id, 'customer_id':customer_id, 'appointment_id':appointment_id};
		if(checkin != undefined){
			data['checkin'] = checkin;
		}
		var callbackArguments = {'panel_id':'#appointment_detail_'+appointment_id , 'timmercount' : 'timmercount_'+ appointment_id , 'timmerdiv' : '#timmerdiv_'+appointment_id , 'status':appt_status};
		dealership.getTemplateFromServer(url_ov_appointment_detail, data, self.refreshAppointmentDetailCallback, callbackArguments);
	};
	
	this.refreshAppointmentDetailCallback = function(response, callbackArguments){
		$(callbackArguments.panel_id).html(response);
		if (callbackArguments.status != undefined ){
			element = document.getElementById(callbackArguments.timmercount);
			min = element.getAttribute('min');
			sec= element.getAttribute('sec');
			dealership.countdown(element ,parseInt(min),parseInt(sec) , callbackArguments.timmerdiv , callbackArguments.status);
		}
	};	
	
	/*
	 * todo: confirm if these function are un-used
	 
	this.updateSingleAppointment = function(id){
		var data = {'id':id};
		var callbackArguments = {'panel_id': '#appointment_'+id};
		dealership.getTemplateFromServer("{% url 'dealership:ov_time_daily_row' %}", data, self.updateSingleAppointmentCallback, callbackArguments);		
	};
	
	this.updateSingleAppointmentCallback = function(response, callbackArguments){
		$(callbackArguments.panel_id).html(response);
	};	
	
	this.updateMeters = function()
	{
		$.ajax({
            url: "{% url 'dealership:meters' %}",
            type: "get",
            success: function(response) {
                alert(response)
            }
        });	
	};
	
	*/
	/*
	 * todo: confirm if removeService function is un-used
	 */
	this.removeService = function(element){
	   	var data = {'id':element.attr("rel")};
        var callbackArguments = {"panel_id":element};
	   	dealership.getDataFromServer(url_remove_service, data, self.removeServiceCallback, callbackArguments);
	};
	
	this.removeServiceCallback = function(data, callbackArguments){
        if(data["status"] == true){
            callbackArguments.panel_id.closest(".ScheduleServiceCont").find('.alert').addClass("hidden");
            callbackArguments.panel_id.closest(".form-group").remove();            
        }else{
            callbackArguments.panel_id.closest(".ScheduleServiceCont").find('.alert').removeClass("hidden");
            callbackArguments.panel_id.closest(".ScheduleServiceCont").find('.alert .details').html("Service not removed")
        }
	};	
	
	this.getAvlAdvisorListCallback = function(data, callbackArguments){
		callbackArguments.panel_id.html("");
		for(i in data["data"]){
			var cls ="pointer";
			var li = $('<li><a class="'+cls+'" rel="'+data["data"][i]['id']+'">'+data["data"][i]['title']+'</a></li>');
			callbackArguments.panel_id.append(li);
		}
	};
	
	this.scroll = function(prefix, callbackArguments, day)
	{
		//var counter = self.add();
		self.totalSlabCallsReturned = self.totalSlabCallsReturned  + 1;
		//console.info(self.totalSlabCallsReturned);
		//console.info(self.totalSlabCalls);
		if(callbackArguments.slab_id == callbackArguments.current_slab || self.totalSlabCallsReturned == self.totalSlabCalls)
		{
			self.animateScroll(callbackArguments.current_slab, day);
			if($(day).length > 0){
				$(callbackArguments.panel_id).scrollLeft($(day).offset().left);
			}			
		 	//if(counter == total)
			//{
				//self.scrollInterval(prefix, day);
			//}		 	
		}	
	};
	
	this.animateScroll = function(current_slab, day)
	{		
		/*
		$('html, body').animate({
	        scrollTop: $(current_slab).offset().top
	 	}, 500);	
	 	*/
	 	if (day === undefined)
	 	{
	 		$("html, body").scrollTo(current_slab);
	 		$(current_slab+' .HeadRow').click();
	 	}
	 	else
	 	{
			$("html, body").scrollTo(day);
	 		$(day+" .panel-group").scrollTo(current_slab);	 			
	 		$(current_slab+" .panel-collapse").addClass('in');
	 		$(current_slab+" .fa").removeClass("fa-plus-circle").addClass('fa-minus-circle');
	 		
	 	}	
	};
	
	this.scrollInterval = function(prefix, day)
	{		
		var now = moment();
		var difference = (((10 - parseInt(now.format('mm')%10)) * 60)-parseInt(now.format('s')))*1000;
		if(self.firstTimerInterval != null) { clearInterval(self.firstTimerInterval); }
		self.firstTimerInterval = setInterval(function(){ 
				current_slab = self.getCurrentSlabForScroll(prefix);
				animateScroll(current_slab, day);
				self.keepScrolling(current_slab, day);
			}, difference);
	};
	
	this.keepScrolling = function(current_slab, day){
		if(self.scrollTimerInterval != null){ clearInterval(self.scrollTimerInterval); }
		self.scrollTimerInterval = setInterval(function(){ 
			clearInterval(firstTimerInterval);
			current_slab = self.getCurrentSlabForScroll(prefix);
			animateScroll(current_slab, day); 
		}, 600000);
	};
	
	this.getCurrentSlabForScroll = function(prefix)
	{
		var now = moment().subtract(10, 'minutes');
		current_slab = prefix+now.format('_YYYY_MM_DD_HH_')+roundTime(now.format('mm'));
		//current_slab = prefix+now.format('_YYYY_M_D_07_00');
		console.info(current_slab);
		return current_slab;
	};
	
	this.add = (function () {
	    var counter = 0;
	    return function () {return counter += 1;}
	});
	
	jQuery.fn.scrollTo = function(elem) { 
		if ($(elem).length > 0){
			$(this).animate({
	        	scrollTop:  $(this).scrollTop() - $(this).offset().top + $(elem).offset().top
	    	}, 500);
	    	return this; 
		}	    
	};	
		
	jQuery.fn.changeAppointment = function() {  
	   	var data = {};
	   	data['id'] = $(this).closest('.appointment_row').attr('rel');
	   	data[$(this).closest('ul').attr('rel')] = $(this).attr('rel');
		dealership.getDataFromServer(url_appointment_create_update, data, self.changeAppointmentCallback);
	};
	
	this.changeAppointmentCallback = function(data, callbackArguments){
		
	};
}
	
function roundTime(mins)
{
	lower = (parseInt(parseInt(mins)/10))*10;
	if(lower<10){ lower = "0"+lower; }
    return lower;
}  
