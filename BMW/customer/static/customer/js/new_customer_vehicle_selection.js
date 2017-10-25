$(document).ready(function(){

});
function NewCustomerVehicleWidget(){
	this.make_control = null;
	this.year_control = null;
	this.vehichle_id_control = null;
	this.vehicles = null
	var self = this;
	this.query_url = null;
	this.image_main_url = null
	this.vehicles = {}
	this.vin_text_input=null;
	self.initialize = function(){
		self.fillAll();
		self.setEventListeners();
	}
	
	self.receiveOcr = function(text){
		if($.trim(text)!=""){
			self.vin_text_input.val(text);
		}else{
			BootstrapDialog.alert('Unable to process the VIN');
		}
		
	}
	
	self.fillAll = function(){
		
		$(self.vehicles).each(function(k,v){
			self.appendUniqueValues(self.make_control,self.vehicles[k]["make__name"]);
			self.appendUniqueValues(self.year_control,self.vehicles[k]["year__name"]);
			
		});
	}
	
	self.appendUniqueValues=function(control,value){
		if (self.valExists(control,value)==false){
			var option = $("<option>");
			option.val(value);
			option.text(value);
			control.append(option);
		}
	}
	
	self.valExists = function(control,value){
		exists=false
		control.find("option").each(function(){
		    if (this.value == value) {
		        exists =  true;
		        return false;
		    }
		});
		return exists
	}
	
	self.disableAll = function(){
		self.make_control.prop("disabled","disabled");

		self.year_control.prop("disabled","disabled");
	
	}
	
	self.clearControl = function(control,controlname){
		control.html("");
		control.append("<option value=''>Select "+controlname+"</option>");
	}
	
	self.disableControl= function(control){
		control.prop("disabled","disabled");
	}
	
	self.enableControl= function(control){
		control.removeProp("disabled");
	}
	
	self.enableAll = function(){
		self.make_control.remoeProp("disabled");

		self.year_control.remoeProp("disabled");

	}
	

	
	self.setEventListeners = function(){
			self.make_control.change(function(){
				var make_value = $(this).val();
				self.clearControl(self.year_control,"Year");


				$(self.vehicles).each(function(k,v){
					if(make_value == self.vehicles[k]["make__name"]){
						self.appendUniqueValues(self.year_control,self.vehicles[k]["year__name"])
					}
				});
				self.enableControl(self.year_control);
			
			});
//			self.model_control.change(function(){
//				self.unsetVehicleId()
//				self.unsetImage();
//				var model_value = $(this).val();
//				var make_value = self.make_control.val()
//				self.clearControl(self.year_control,"Year");
//				self.clearControl(self.trim_control,"Trim");
//				$(self.vehicles).each(function(k,v){
//					if(model_value == self.vehicles[k]["model__name"] &&
//							make_value == self.vehicles[k]["make__name"] ){
//						self.appendUniqueValues(self.year_control,self.vehicles[k]["year__name"])
//					}
//				});
//				self.enableControl(self.year_control);
//				self.disableControl(self.trim_control);
//			});
//			self.year_control.change(function(){
//				self.unsetVehicleId()
//				self.unsetImage();
//				var model_value = self.model_control.val()
//				var make_value = self.make_control.val()
//				var year_value =  $(this).val();
//				
//				$(self.vehicles).each(function(k,v){
//					if(year_value == self.vehicles[k]["year__name"] &&
//						model_value == self.vehicles[k]["model__name"] &&
//						make_value == self.vehicles[k]["make__name"] )
//					{
//						self.setVehicleId(self.vehicles[k]["id"])
//						
//						self.setImage(self.vehicles[k]["mainimage"])
////						self.appendUniqueValues(self.trim_control,self.vehicles[k]["vehicle__trim"])
//						
//					}
//				});
//				self.enableControl(self.trim_control);
//			});
//			self.trim_control.change(function(){
//				self.unsetVehicleId()
//				self.unsetImage();
//				var model_value = self.model_control.val()
//				var make_value = self.make_control.val()
//				var year_value =  self.year_control.val();
//				var trim_value =  $(this).val();
//				$(self.vehicles).each(function(k,v){
//					if(year_value == self.vehicles[k]["vehicle__year"] &&
//						model_value == self.vehicles[k]["vehicle__model"] &&
//						make_value == self.vehicles[k]["vehicle__make"] && trim_value ==  self.vehicles[k]["vehicle__trim"])
//					{
//						self.setVehicleId(self.vehicles[k]["vehicle_id"])
//						
//						self.setImage(self.vehicles[k]["vehicle__mainimage"])
//					}
//				});
//			});
			
	}
}