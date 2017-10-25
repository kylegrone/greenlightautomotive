$(document).on('submit', '#walkinappointment', function(e){
	var data = new FormData($(this).get(0));
	$('#loading_page').show();
	$.ajax({
	    url: walkin_appointment,
	    type: "POST",
	    data: data,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) { 
	    	if(data["success"]==true){
		    	var date = moment();
				window.mobilecheckinAppointment = new MobileCheckinAppointment();
				window.mobilecheckinAppointment.setEventListeners();	
				window.mobilecheckinAppointment.loadAppointmentSlots(date);
				$('.walkin').modal('toggle');
		    	$('#walkinappointment')[0].reset();
	    	}else{
	    		if (Object.prototype.toString.call(data["message"]) === '[object Array]'){
		    		var errmsg = "<ul>";
		    		for(i=0; i<data["message"].length; i++){
		    			$('input[name="'+data["message"][i][0]+'"]').addClass('inputTxtError');
		    			errmsg += "<li>"+data["message"][i][1]+"</li>";
		    		}
		    		errmsg +="</ul>";
	    		}
	    		else{
	    			errmsg = data["message"]
	    		}
                 $('.errmsg').html(errmsg);
                 $('.alert-danger').show();
	    	}
	    	$('#loading_page').hide();
	    },
	  error: function(data){
		  $('.errmsg').html("Error Occured While Booking Appointment");
          $('.alert-danger').show();
		  $('#loading_page').hide();
	  }
	});
	e.preventDefault();
});

$(document).on('click' , '.search_customer', function(){
	$('#loading_page').show();
	if ($('#phonenumber').val()){
		$.post(walkin_search , {'phone': $('#phonenumber').val()} ,function(data){
			if(data["success"]==true){
				$('.cust-search-error').hide();
				$('#customer_id').val(data['customer']['id'])
				$('#first_name_id').val(data['customer']['fname']);
				$('#last_name_id').val(data['customer']['lname']);
				$('#id_phone_number_1').val(data['customer']['phone']);
				$('#id_email_1').val(data['customer']['email']);
				$('#phonenumber').val("");
				if(data['customer']['vehicles'].length>0){
					$('.customer_pveh').show();
					vehselect = document.getElementById('cus_veh');
					for(i=0; i<data['customer']['vehicles'].length; i++){
						var veh = new Option(data['customer']['vehicles'][i]['name'], data['customer']['vehicles'][i]['id']);
						vehselect.options[vehselect.options.length] = veh;
						veh.setAttribute('vin-key',data['customer']['vehicles'][i]['vin']);
						veh.setAttribute('year-val',data['customer']['vehicles'][i]['year_val']);
						veh.setAttribute('model-val',data['customer']['vehicles'][i]['model_val']);
						veh.setAttribute('make-val',data['customer']['vehicles'][i]['make_val']);
						 
					}
				 }
				$('#loading_page').hide();
			}else{
				$('.cust-search-error').show();
				$('#loading_page').hide();
			}
			
		}).fail(function(){
			$('.cust-search-error').show();
			$('#loading_page').hide();
		});
	}
});

$("[data-hide]").on("click", function(){
    $(this).closest("." + $(this).attr("data-hide")).hide();
    return false;
});

$(document).on('click', '.wlkinclose' , function(){
	$('#phonenumber').val("");
	$('#walkinappointment')[0].reset();
	$('.customer_pveh').hide();
});
$('.walkin').on('hidden.bs.modal', function () {
    // do something…
	$('#phonenumber').val("");
	$('#walkinappointment')[0].reset();
	$("#customer_id").val("")
	$('.customer_pveh').hide();
});



$(document).on('change', '#cus_veh' , function(){
	$('#id_vin').val($('option:selected', this).attr('vin-key'));
	$('.oldvehyear').val($('option:selected', this).attr('year-val'));
	$('.oldvehmodel').val($('option:selected', this).attr('model-val'));
	$('.oldvehmake').val($('option:selected', this).attr('make-val'));
	$('#vehicle_id_field').val($(this).val());
});