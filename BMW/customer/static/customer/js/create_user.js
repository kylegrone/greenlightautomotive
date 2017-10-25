$(document).ready(function(){
var user_field_error = true;
	$('#form_create_user #new').focusout(function(){
		
		$('#form_create_user #new').removeClass("error_input");
		if($(this).val().length > 5) { 
				$(".tick #char").addClass("check");
				
		}
		else { $(".tick #char").removeClass("check") ;$('#form_create_user #new').addClass("error_input");}	
		
		if($(this).val().match(/[A-Z]/)){$(".tick #uper").addClass("check"); }
		else {$(".tick #uper").removeClass("check")}
		
		if($(this).val().match(/[a-z]/)){$(".tick #lower").addClass("check"); }
		else {$(".tick #lower").removeClass("check");$('#form_create_user #new').addClass("error_input");}
		
		if($(this).val().match(/[0-1]/)){$(".tick #number").addClass("check"); }
		else {$(".tick #number").removeClass("check");$('#form_create_user #new').addClass("error_input");}
		
		if($(this).val().match(/[!@#$%^&*()+=\';,.\/{}|":<>?~_-]/)){$(".tick #symbol").addClass("check"); }
		else {$(".tick #symbol").removeClass("check");$('#form_create_user #new').addClass("error_input");}
		
		if($(this).val() == $('#form_create_user #confirm').val()){ $(".tick #match").addClass("check") ; }
		else { $(".tick #match").removeClass("check"); }
	});
    
	$('#form_create_user #confirm').focusout(function(){
		$('#form_create_user #confirm').removeClass("error_input");
		if($(this).val() == $('#form_create_user #new').val()){ $(".tick #match").addClass("check") ; }
		else { $(".tick #match").removeClass("check") ;$('#form_create_user #confirm').addClass("error_input");}	
	});
	
	$('#form_create_user').submit(function(event){	
		
		var username = $("#user_name_id");
		if($('.tick .check').size() < 6 || username.data("error")==true) {
			BootstrapDialog.alert('Pleae fill out the form with out errors.');
			event.preventDefault();
		}	
		if($('.tick .check').size() < 6 ){
			$('#form_create_user #new').addClass("error_input");
		}
	});
	
	$("#user_name_id").focusout(function(){
		$(this).removeClass("error_input");
		$(this).data("error",false);
		$("#user_error_div").hide();
		var username = $(this).val();
		if ($.trim(username)=="" || $.trim(username).length <6){
			$(this).data("error",true);
			$(this).addClass("error_input");
			$("#user_error_div").find(".error_msg").html("Username must be atleast 6 charachters");
			$("#user_error_div").show()
		}else{
			$("#loading_page").show();
			$.ajax({
				url:$("#check_user_exist_id").data("url"),
				data:{
					"username":username,
				},
				success:function(msg){
					if (msg.success==true){
						$(this).addClass("error_input");
						$(this).data("error",true);
						$("#user_error_div").find(".error_msg").html("Username already exists");
						$("#user_error_div").show()
					}
					$("#loading_page").hide();
				},
				error:function(){
					$("#loading_page").hide();
				},
			})
		}
	})
	
})