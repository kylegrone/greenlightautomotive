$(document).ready(function(){
	var min = $('#countdown').attr('min');
	var sec = $('#countdown').attr('sec');
	countdown( "countdown",parseInt(min),parseInt(sec));
	timmer(0);
	
});
function twodigits( n )
{
    return (n <= 9 ? "0" + n : n);
}

function timmer(count){
	counter = count;
	counter++;//increment the counter by 1
	element = document.getElementById('timmer_checkin');
	element.innerHTML = twodigits(Math.floor(counter/60 )) + ':' + twodigits(counter%60 );
	setTimeout ("timmer("+counter+")", 1000 )
}
function countdown( elementName, minutes, seconds )
{
    var element, endTime, hours, mins, msLeft, time;

    function twoDigits( n )
    {
        return (n <= 9 ? "0" + n : n);
    }

    function updateTimer()
    {
        msLeft = endTime - (+new Date);
        if ( msLeft < 1000 ) {
        	time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            $('#counter_status').removeClass('text_blue');
            $('#counter_status').addClass('text_red');
            var snd = new Audio(beep_url);
            snd.play();
        } else {
            time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
        }
    }

    element = document.getElementById( elementName );
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    updateTimer();
}

$(document).on('click' , '#odoscreen' , function(){
	$('#loading_page').show();
	$.ajax({
	    url: get_odo,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	return false
});
$(document).on('click' , '#walkarscreen' , function(){
	$('#loading_page').show();
	$.ajax({
	    url: get_walkaround,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('.carousel-inner').find('img').each(function(){
				    $(this).mapster(
					       {
					       		fillOpacity: 0.4,
					       		fillColor: "d42e16",
					       		strokeColor: "3320FF",
					       		strokeOpacity: 0.8,
					       		strokeWidth: 4,
					       		stroke: true,
					            isSelectable: true,
								singleSelect: false,
								isDeselectable: true,
					            mapKey: 'name',
					            listKey: 'name',
					            onClick: function (e) {
					            	/*console.log(e);
					            	if (e.key === 'RR' || e.key === 'RF' || e.key === 'LR' || e.key === 'LF'){
					            		$('#selecttires').removeClass('hidden');
					            		$('input[value=Tires]').attr('checked',true);
					            		 $(".wlktype label").removeClass("active");
					            		 $(".wlktype label[name=tires]").addClass('active');
					            		 $(this).addClass("active");
					            	}
					            	else{
					            		$('#selecttires').addClass('hidden');
					            		$('input[value=Tires]').attr('checked',false);
					            		$('input[value=Scratch]').attr('checked',true);
					            		$(".wlktype label").removeClass("active");
					            		$(".wlktype label[name=scratch]").addClass('active');
					            	}*/
					            }
					        });
				    	//$(this).mapster('resize',700,532,0); 
			});
	    	var is_safari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
	    	if (is_safari){
	    		$('#cameracontorls').html("<label for='safarifile'>\
	            		<div class='CamBtn mb-10'><span id='safaricamera' class='glyphicon glyphicon-camera pointer'></span></div>\
	        			</label>\
	        			<button id='canclesafaricam' class='btn btn-xs btn-danger hidden' type='button'><span aria-hidden='true' class='glyphicon glyphicon-camera'></span>Cancel</button>\
	        			<input type='file' id='safarifile' accept='image/*' style='display:none'/>");
	    	}
			   $('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	return false
});
$(document).on('click' , '#walkarmedia' , function(){
	$('#loading_page').show();
	fillVehicleImages($('#checkincurrent'));
	return
	$.ajax({
	    url: get_walkaround_media,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	return false
});
function fillVehicleImages(fill_area){
	$.ajax({
	    url: get_walkaround_media,
	    type: "GET",
	    success: function(data) {
	    	fill_area.html(data);
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
}
$(document).on('click' , '#walkarnotes' , function(){
	$('#loading_page').show();
	$.ajax({
	    url: get_walkaround_notes,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	return false
});
$(document).on('click' , '#serscreen' , function(){
	$('#loading_page').show();
	$.ajax({
	    url: get_service_repair,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	return false
});
$(document).on('click' , '#reviewscreen' , function(){
	$('#loading_page').show();
	$.ajax({
	    url: get_review,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#customer_signature').sketch();
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	
	return false
});

$(document).on('click','.saveodo',function(){
	$('#loading_page').show();
	$.post(get_odo_history,{'odo' : $('#odometer_manual').val(),
	"odo_data":$("#odo_data").val()	
	},function(data){
	      $('#odometerhistory').html(data);
	      $('#odometerhistory').removeClass('hidden');
	      $('#loading_page').hide();
	      $('.successbox').html("Odo# Saved Succesfully");
	      $('.successbox').show();
	      $('.successbox').fadeOut(5000);
    }).fail(function(){
		$('#loading_page').hide();
    	$('.errorbox').show();
    	$('.errorbox').fadeOut(5000);
	});
	return false
});

$(document).on('click','.savevin',function(){
	$('#loading_page').show();
	$.post(save_vin,{'vin' : $('#vin_manual').val(),
		"vin_data":$("#vin_data").val()	
	},function(data){
	      $('#loading_page').hide();
	      $('.successbox').html("Vin# Saved Succesfully");
	    	$('.successbox').show();
	    	$('.successbox').fadeOut(5000);
    }).fail(function(){
		$('#loading_page').hide();
		$('.errorbox').show();
    	$('.errorbox').fadeOut(5000);
    	
	});
	return false
});

$(document).on('change','#select_ser_rep', function(){
	if($(this).val()){
		$('#loading_page').show();
		$.post(get_service_repair_list,{'type' : $(this).val()},function(data){
		      $('#servicerepairlist').html(data);
		      $('#loading_page').hide();
	    }).fail(function(){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		});
	}
});


$(document).on('click','.addserrep',function(){
	$('#loading_page').show();
	$.post(add_service_repair,{'id' : $(this).attr('id'),
			"price":parseFloat($("#"+$(this).data("priceinput")).val()).toFixed(2),"desc":$("#"+$(this).data("noteobj")).val()
	},function(data){
	      $('#apptservicelist').html(data);
	      $('#loading_page').hide();
	}).fail(function(){
		$('#loading_page').hide();
    	$('.errorbox').show();
    	$('.errorbox').fadeOut(5000);
	});
});

$(document).on('click','.removeserrep',function(){
	$('#loading_page').show();
	$.post(remove_service_repair,{'id' : $(this).attr('id')},function(data){
	      $('#apptservicelist').html(data);
	      $('#loading_page').hide();
	}).fail(function(){
		$('#loading_page').hide();
    	$('.errorbox').show();
    	$('.errorbox').fadeOut(5000);
	});
});
$(document).on('click','.updateservicerepair',function(){
	$('#loading_page').show();
	$.post(update_service_repair,{'id' : $(this).attr('id'),
	"price":$("#"+$(this).data("priceobj")).val()	,"desc":$("#"+$(this).data("noteobj")).val()	
	},function(data){
	      $('#apptservicelist').html(data);
	      $('#loading_page').hide();
	}).fail(function(){
		$('#loading_page').hide();
    	$('.errorbox').show();
    	$('.errorbox').fadeOut(5000);
	});
});

$(document).on('click','.searchserrep' , function(){
	$('#loading_page').show();
	if($('input[name=searchserrepname]').val()){
		$.post(get_by_name_service_repair,{'key' : $('input[name=searchserrepname]').val()},function(data){
			$('#servicerepairlist').html(data);
			$('#loading_page').hide();
		}).fail(function(){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		});
	}
});
$(document).on('click','.addnotes' , function(){
	$('#loading_page').show();
	var formData =  new FormData();
	formData.append('note' , $('input[name=notes]').val());
	formData.append('image_name' , $('input[name=photoname]').val());
	formData.append('type' ,$('input[name=walkaroundtype]:checked').val())
	formData.append('other_category' ,$('#wlkscat').val())
	formData.append('other_type' ,$('#wlktyp').val())
	/*formData.append('RR' ,$('#RR').val())
	formData.append('RF' ,$('#RF').val())
	formData.append('LR' ,$('#LR').val())
	formData.append('LF' ,$('#LF').val())*/
	if($('#photo').attr('src') && $('#photo').attr('src')!=""){
		formData.append('image', $('#photo').attr('src'));
		$.ajax({
		    url: add_walkaround_notes,
		    type: "POST",
		    data: formData,
		    cache: false,
		    processData: false,
		    contentType: false,
		    success: function(data) {
		    	$('#loading_page').hide();
		    	$('.successbox').html("Notes Added Successfully");
		    	$('.successbox').show();
		    	$('.successbox').fadeOut(5000);
		    	fillVehicleImages($('#vehicle_image_list'));
		    	return
		    	
		    },
		    error : function(data){
		    	$('#loading_page').hide();
		    	$('.errorbox').show();
		    	$('.errorbox').fadeOut(5000);
		    }
		});
	}else{
		
			$('#loading_page').show();
			var activediv = $('.carousel-inner').find('.active')
			html2canvas([activediv[0]], {  
			proxy : image_proxy,
	        onrendered: function(canvas)  
	        {
	            img = canvas.toDataURL()
	            var formData =  new FormData();
				formData.append('note' , $('input[name=notes]').val());
				formData.append('image_name' , $('input[name=photoname]').val());
				formData.append('type' ,$('input[name=walkaroundtype]:checked').val());
				formData.append('other_category' ,$('#wlkscat').val());
				formData.append('other_type' ,$('#wlktyp').val());
				/*formData.append('RR' ,$('#RR').val());
				formData.append('RF' ,$('#RF').val());
				formData.append('LR' ,$('#LR').val());
				formData.append('LF' ,$('#LF').val());*/
				formData.append('image', img);
				console.log(formData);
	            $.ajax({
	        	    url: add_walkaround_notes,
	        	    type: "POST",
	        	    data: formData,
	        	    cache: false,
	        	    processData: false,
	        	    contentType: false,
	        	    success: function(data) {
	        	    	$('#loading_page').hide();
	        	    	$('.successbox').html("Notes Added Successfully");
	    		    	$('.successbox').show();
	    		    	$('.successbox').fadeOut(5000);
	        	    },
	        	    error: function(data){
	        	    	$('#loading_page').hide();
	    		    	$('.errorbox').show();
	    		    	$('.errorbox').fadeOut(5000);
	        	    }
	        	});
	        }
	    });
	}
});

$(document).on('click','.wlktype',function(){
	$('input[name=notes]').val("");
	$('input[name=photoname]').val("");
	if ($('input[name=walkaroundtype]:checked').val()== 'Other'){
		$('#selecttires').addClass('hidden')
		$('#selectother').removeClass('hidden');
	}
	else if ($('input[name=walkaroundtype]:checked').val() == 'Tires'){
		$('#selectother').addClass('hidden');
		$('#selecttires').removeClass('hidden')
	}
	else{
		$('#selectother').addClass('hidden');
		$('#selecttires').addClass('hidden');
	}
});

$(document).on('change','#wlkcusveh', function(){
	if($(this).val()){
		$('#loading_page').show();
		/*$.post(get_selected_vehicle,{'id' : $(this).val()},function(data){
		      $('#vehicle_details').html(data);
		      $('#loading_page').hide();
	    }).fail(function(){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		});*/
		$.post(get_selected_vehicle_map,{'id' : $(this).val()},function(data){
		      $('#vehicle_image_map').html(data);
		      $('.carousel-inner').find('img').each(function(){
				    $(this).mapster(
					       {
					       		fillOpacity: 0.4,
					       		fillColor: "d42e16",
					       		strokeColor: "3320FF",
					       		strokeOpacity: 0.8,
					       		strokeWidth: 4,
					       		stroke: true,
					            isSelectable: true,
								singleSelect: false,
								isDeselectable: true,
					            mapKey: 'name',
					            listKey: 'name',
					            onClick: function (e) {
					            	console.log(e);
					            	/*if (e.key === 'RR' || e.key === 'RF' || e.key === 'LR' || e.key === 'LF'){
					            		$('#selecttires').removeClass('hidden');
					            		$('input[value=Tires]').attr('checked',true);
					            		 $(".wlktype label").removeClass("active");
					            		 $(".wlktype label[name=tires]").addClass('active');
					            		 $(this).addClass("active");
					            	}
					            	else{
					            		$('#selecttires').addClass('hidden');
					            		$('input[value=Tires]').attr('checked',false);
					            		$('input[value=Scratch]').attr('checked',true);
					            		$(".wlktype label").removeClass("active");
					            		$(".wlktype label[name=scratch]").addClass('active');
					            	}*/
					            }
					        });
				    	//$(this).mapster('resize',700,532,0); 
			});
		      var is_safari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
		    	if (is_safari){
		    		$('#cameracontorls').html("<label for='safarifile'>\
		            		<div class='CamBtn mb-10'><span id='safaricamera' class='glyphicon glyphicon-camera pointer'></span></div>\
		        			</label>\
		        			<button id='canclesafaricam' class='btn btn-xs btn-danger hidden' type='button'><span aria-hidden='true' class='glyphicon glyphicon-camera'></span>Cancle</button>\
		        			<input type='file' id='safarifile' accept='image/*' style='display:none'/>");
		    	}
			   $('#loading_page').hide();
		}).fail(function(){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		});
	}
});
$(document).on('click','.addinitials',function(){
	$('#loading_page').show();
	$.post(add_initials,{'initials' : $('input[name=initials]').val() , 'type':$('input[name=walkaroundtype]:checked').val()},function(data){
		$('#loading_page').hide();
		$('.successbox').html("Initials Added Successfully");
    	$('.successbox').show();
    	$('.successbox').fadeOut(5000);
		
	}).fail(function(){
		$('#loading_page').hide();
    	$('.errorbox').show();
    	$('.errorbox').fadeOut(5000);
	});
	return false;
});
$(document).on('click','.acceptappointment',function(){
	var canvas = document.getElementById ("customer_signature");
	var blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;
	if ($('#signature').val() == ""){
		alert("Customer Name is Required");
	}
	else if(canvas.toDataURL()== blank.toDataURL()){
		alert("Customer Signature is Required");
	}
	else{
		$('#loading_page').show();
		$.post(accept_appointment,{'sign' : canvas.toDataURL() , 'send_email' : $('#preorderemail').is(':checked')},function(data){
			$('#loading_page').hide();
			window.location.href = main_page;
		}).fail(function(){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
	    	window.location.href = main_page;
		});
	}
});
$(document).on('click','.cancelappointment',function(){
		$('#loading_page').show();
		$.post(cancel_appointment,{},function(data){
			$('#loading_page').hide();
			window.location.href = main_page;
		}).fail(function(){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
	    	window.location.href = main_page;
		});
});
$(".left_nav li").on("click", function() {
    $(".left_nav li").removeClass("active");
    $(this).addClass("active");
  });

$(document).on("click", ".sr-label:not(:has(input))", function(event){
	var newHTML  = '<input name="'+$(this).attr('name')+'" type="text" value="'+$(this).text()+'" class="form-control">';
	$(this).html(newHTML)
	return false;
});
$(document).on('click','.erase' , function(event){
	element = document.getElementById ("customer_signature");
	context=element.getContext("2d");
	context.clearRect (0, 0, element.width, element.height);
	$('#customer_signature').sketch().actions = [];
});
$(document).on('click','.cancelinitials',function(event){
	$('input[name=initials]').val("");
});

$(document).on('click' , '#tirethread' , function(){
	$('#loading_page').show();
	$.ajax({
	    url: get_tire_thread,
	    type: "GET",
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#loading_page').hide();
	    },
		error: function(data){
			$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
		}
	});
	return false
});
$(document).on('click' ,'.tireaddnotes', function(){
	$('#loading_page').show();
	var formData =  new FormData();
	formData.append('notes' ,$('#TireAddNotes').val())
	formData.append('RR' ,$('#RR').val())
	formData.append('RF' ,$('#RF').val())
	formData.append('LR' ,$('#LR').val())
	formData.append('LF' ,$('#LF').val())
	$.ajax({
	    url: add_tire_notes,
	    type: "POST",
	    data: formData,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) {
	    	$('#checkincurrent').html(data);
	    	$('#loading_page').hide();
	    	$('.successbox').html("Notes Added Successfully");
	    	$('.successbox').show();
	    	$('.successbox').fadeOut(5000);
	    },
	    error : function(data){
	    	$('#loading_page').hide();
	    	$('.errorbox').show();
	    	$('.errorbox').fadeOut(5000);
	    }
	});
});
$(document).on('click','#deleteimage',function(){
	console.log("hello");
});

$(document).on('change', '.two_decimal_number' , function(){
	$(this).val(parseFloat($(this).val()).toFixed(2));
});
