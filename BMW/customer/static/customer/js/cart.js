function Cart(){
	this.url  = "";
	self = this
	this.cart_container = null;
	this.appointment_id = null;
	this.dealer_code = null
	this.fillCart= function(){
		
		if (self.cart_container!=null){
			self.cart_container.html("Loading...");
			$.ajax({
				url:this.url,
				data:{"appointment_id":self.appointment_id,"dealer_code":self.dealer_code},
				success:function(resp){
					self.cart_container.html(resp)
				},errpr:function(){
					console.info("errror")
				}
				
			})
		}
		
	}
	$("#pop").on("click", function() {
		   $('#imagepreview').attr('src', $('#imageresource').attr('src')); // here asign the image to the modal when the user click the enlarge link
		   $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
		});
	
}