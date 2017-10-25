$(document).ready(function(){
	/**
	 * this event listener is used to handle the toggle event of the add vehicle
	 * 
	 */
	
	
	$('.collapse_button_trigger').click(function(){
		$(this).parent().find(".collapse_button").trigger("click");
	});
	
	
	$("body").on("click",'.collapse_button',function(){
		toggleContainer($(this).closest(".collaps_main_container"))
	});
	
	$("body").on("click",".imgpopup", function() {
			
		   $('#imagepreviewmodal').attr('src', $(this).attr('src')); // here asign the image to the modal when the user click the enlarge link
		   $('#modelimagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
		});
	$("body").on("mouseover",".service_menu li",function(){
		$(this).find(".dropdown-menu").show()
	});
	$("body").on("mouseout",".service_menu li",function(){
		
		$(this).find(".dropdown-menu").hide()
	});
	$(document).ready(function(){
	    $('[data-toggle="tooltip"]').tooltip(); 
	});
})
function closeContainers(){
		
		$('.collapse_button').each(function(i,obj){
			
			closeContainer($(this).closest(".collaps_main_container"))
		});
}
	
function openContainer(container){
	closeContainers();
	var collapseButton = container.find('.collapse_button')
	var minus_class ="fa-minus-square-o" //;$(this).data("min-class");
	var plus_class ="fa-plus-square-o" //$(this).data("plus-class");
	if (collapseButton.data("minclass")!="" && typeof collapseButton.data("minclass") !="undefined"){
		minus_class = collapseButton.data("minclass");
		plus_class = collapseButton.data("plusclass");
	}
		
//		container.closest(".collaps_main_container").find(".collapsable_div").css("display","block");
		container.find(".collapsable_div").css('display',"block");
		collapseButton.removeClass(plus_class);
		collapseButton.addClass(minus_class);
}
	
function closeContainer(container){
	var collapseButton = container.find('.collapse_button')
	var minus_class ="fa-minus-square-o" //;$(this).data("min-class");
	var plus_class ="fa-plus-square-o" //$(this).data("plus-class");
	if (collapseButton.data("minclass")!="" && typeof collapseButton.data("minclass") !="undefined"){
		minus_class = collapseButton.data("minclass");
		plus_class = collapseButton.data("plusclass");
	}
	
	container.find(".collapsable_div").css("display","none");
	collapseButton.removeClass(minus_class);
	collapseButton.addClass(plus_class);
	
}
	
function toggleContainer(container){
		if(container.find(".collapsable_div").css("display") == "block"  ){
			closeContainer(container);
		}else{
			openContainer(container);
		}
}