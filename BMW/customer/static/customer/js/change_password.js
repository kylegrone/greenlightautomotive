$(document).ready(function(){

	$('#form_pass #new').focusout(function(){
		console.info($(this).val().length);
		
		if($(this).val().length > 5) { $(".tick #char").addClass("check"); }
		else { $(".tick #char").removeClass("check") }	
		
		if($(this).val().match(/[A-Z]/)){$(".tick #uper").addClass("check"); }
		else {$(".tick #uper").removeClass("check")}
		
		if($(this).val().match(/[a-z]/)){$(".tick #lower").addClass("check"); }
		else {$(".tick #lower").removeClass("check")}
		
		if($(this).val().match(/[0-1]/)){$(".tick #number").addClass("check"); }
		else {$(".tick #number").removeClass("check")}
		
		if($(this).val().match(/[!@#$%^&*()+=\';,.\/{}|":<>?~_-]/)){$(".tick #symbol").addClass("check"); }
		else {$(".tick #symbol").removeClass("check")}
		
		if($(this).val() == $('#form_pass #confirm').val()){ $(".tick #match").addClass("check") ; }
		else { $(".tick #match").removeClass("check") }
	});
    
	$('#form_pass #confirm').focusout(function(){
		if($(this).val() == $('#form_pass #new').val()){ $(".tick #match").addClass("check") ; }
		else { $(".tick #match").removeClass("check") }	
	});
	
	$('#form_pass').submit(function(event){			
		if($('.tick .check').size() < 6){
			event.preventDefault();
		}			
	});
	
})