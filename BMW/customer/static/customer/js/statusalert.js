$(document).on('click','.submitapproval',function(){
	if($('input[name=signature]').val() == ""){
		alert("Signature is required");
	}
	else{
		$('#loading_page').show();
		var data = [];
		$(':radio:checked').each(function(){
			var rec = {};
			rec['id'] = $(this).attr("name");
			rec['val'] = $(this).val();
			data.push(rec);
		})
		data = JSON.stringify(data);
		console.log(data);
		$.post(approve_status ,{'data': data , email_check: $("#status_email").prop('checked')}, function(data){
			$('#loading_page').hide();
			$('.status_successbox').html("Recommendation Status Set Successfully");
			$('#status_notfy').html('<Strong class="text-danger">Recommendation Status has been set successfully. Your Auto will be ready for pick-up soon.</strong>')
	    	$('.status_successbox').show();
	    	$('.status_successbox').fadeOut(5000);
		}).fail(function(){
			$('#loading_page').hide();
	    	$('.status_errorbox').show();
	    	$('.status_errorbox').fadeOut(5000);
		});
	}
});
$(document).on('click','.creditinfo',function(){
	$('#loading_page').show();
	$.post(reply_status ,{'data':""}, function(data){
		$('#loading_page').hide();
		var obj = JSON.parse(data)
		if (obj.message){
			$('#reply_div').html(obj.message);
			$('.payment_details').modal('toggle');
		}
		else{
			window.location.href = obj.data.redirect;
		}
    	
	}).fail(function(){
		$('#loading_page').hide();
    	$('.status_errorbox').show();
    	$('.status_errorbox').fadeOut(5000);
	});
	return false;
});

$(document).on('click', '.canclepayment', function(){
	$('.payment_details').modal('toggle');
})