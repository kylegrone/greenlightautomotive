$(document).ready(function(){
	
//	$("body").on("click",".del_vehicle",function(e){
//		
//		var del_obj = $(this);
//		var con = confirm("Are you sure you want to delete this vehicle.")
//		if(con){
//			
//			window.location = del_obj.data("href");
//		}
//		
//	})
	$('#confirm-delete-vehicle').on('show.bs.modal', function(e) {
	    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
	});
});

function VehicleSearchWidget(){
	var self = this
	this.search_callback = null
	this.search_box = $("#searchbox_vehicle");
	this.all_vehicles = null
	
	this.setVehicles = function(vehicles){
		
		self.all_vehicles = vehicles;
	}
	this.setEvents=function(){
		
		self.search_box.keypress(function(e){
			
			 if(e.which == 13) {
				var temp_vehciles = {} //self.all_vehicles;
				var val_search = self.search_box.val().toLowerCase();
				
				var vehiles_length = Object.keys(self.all_vehicles).length
				if(vehiles_length>0){
					
					$.each(self.all_vehicles,function(k,v){
						var tmp_vehicle = self.all_vehicles[k]
						var vehicle_tmpname = tmp_vehicle["model__name"]+" "+tmp_vehicle["make__name"]+" "+tmp_vehicle["year__name"]
						vehicle_tmpname = vehicle_tmpname.toLowerCase()
						if(vehicle_tmpname.indexOf(val_search)>-1){
							temp_vehciles[k] = v
						}
						
					});
					
					if(typeof self.search_callback!="undefined"){
						
						self.search_callback(temp_vehciles)
					}
				}
			 }
		});
	}

}
function VechileSelection(){
	this.vehicles= null;
	this.models_container = null;
	this.template = null;
	this.current_vehicle_id = null
	this.after_fill_method = null
	this.pagination_container= null;
	var self = this;
	self.vehicles_limit =8;
	self.current_page = 1;
	this.base_url = "";
	this.selectionListner = [];
	this.vehicle_ids_list = []
	this.addSelectionListener = function(list){
		self.selectionListner.push(list)
	}
	
	this.callSelectionListener = function(id){
		$.each(self.selectionListner,function(k,v){
				v(id);
		})
	}
	
	
	self.initialFill = function(vehicles,from_vin){
		
		self.vehicle_ids_list = []
		if(typeof from_vin !="undefined" && vehicles.length == 1){
			self.current_vehicle_id = vehicles[0]["id"]
		}
		self.vehicle_ids_list = Object.keys(vehicles)
		if(typeof self.current_vehicle_id !="undefined" && self.current_vehicle_id !=0 
				&& self.vehicle_ids_list.length>0
				&& $.inArray(""+self.current_vehicle_id,self.vehicle_ids_list) > -1
		){
			self.vehicle_ids_list.unshift(""+self.current_vehicle_id);
		}
		self.vehicles = vehicles;
		self.current_page = 1;
		self.fillModels(vehicles);
		self.setPaging();
		self.setCurrentVehicle();
		
	}
	
	self.setCurrentVehicle = function(){
		$(".model_class").each(function(){
			var vid = $(this).data("vid");
			if (vid == self.current_vehicle_id){
				self.setSelectedModel($(this));
			}
		});
	}
	
	
	self.fillModels = function(vehicles ){
		
		$(self.models_container).html("")
		
		
		var offset = self.getOffset();
		var count = 0;
		var added_count = 0;
		if(self.vehicle_ids_list.length > 0){
			$.each(self.vehicle_ids_list,function(k,vehicle_id){
				vehicle = self.vehicles[vehicle_id]
						if(count >=offset){
							if (added_count< self.vehicles_limit){
								var model_template = $($(self.template).html())
								model_template.find(".thumbnail_inner").prop("src",self.base_url+vehicle["mainimage"]);
								model_template.find(".make_label").html(vehicle["make__name"]);
								model_template.find(".year_label").html(vehicle["year__name"]);
								model_template.find(".model_label").html(vehicle["model__name"]);
								model_template.data("vid",vehicle["id"]);
								$(self.models_container).append(model_template);
								added_count++;
							}
						}
						count++;
			});	
		}
		
		
	}
	
	self.setPaging = function(vehicles){
		var total_pages = self.getTotalPages();
		$(self.pagination_container).html("")
		if(total_pages>1){
			$(self.pagination_container).append(
					"<li class='prev_pagination'><a  aria-label='Previous'><span aria-hidden='true'>«</span></a></li>"		
			)
		}
		for (var i=1;i<=total_pages;i++){
				$(self.pagination_container).append("<li><a>"+i+"</a></li>");
		}
		if(total_pages>1){
				$(self.pagination_container).append(
						"<li class='next_pagination '><a  aria-label='Next'><span aria-hidden='true'>»</span></a></li>"		
				)
		}
		self.setActive()
		
	}
	
	self.setEventListener = function(){
		$("body").on("click",self.pagination_container+" li:not(.disabled)",function(){
			if($(this).hasClass("next_pagination")){
				var current_page = parseInt(self.current_page) + 1
			}else if($(this).hasClass("prev_pagination")){
				var current_page = parseInt(self.current_page) - 1
			}else{
				var current_page = $(this).text();
			}
			self.current_page = current_page;
			self.fillModels(self.vehicles);
			var total_pages = self.getTotalPages();
			self.setActive();
			self.setCurrentVehicle();
		});
		$("body").on("click",".model_class",function(){
			self.setSelectedModel($(this));
		});
	}
	
	self.setSelectedModel = function(th){
		$(".model_class .thumbnail").removeClass("selected");
		self.callSelectionListener(th.data("vid"));
		$("#vehicle_id_field").val();
		th.find(".thumbnail").addClass("selected");
	}
	
	self.setActive = function(){
		$(self.pagination_container+" li").removeClass("active");
		var total_pages = self.getTotalPages();
		$(self.pagination_container+" li").each(function(k,v){
			if($(this).text()==self.current_page){
				$(this).addClass("active");
			}
		})
		if(self.current_page == total_pages){
			$(self.pagination_container+" li.next_pagination").addClass("disabled");
		}else{
			$(self.pagination_container+" li.next_pagination").removeClass("disabled");
		}
		if(self.current_page == 1){
			$(self.pagination_container+" li.prev_pagination").addClass("disabled");
		}else{
			$(self.pagination_container+" li.prev_pagination").removeClass("disabled");
		}
	}
	
	
	self.getOffset = function(){
		var total_pages = self.getTotalPages();
		var offset = ((self.current_page * self.vehicles_limit) - self.vehicles_limit) ;
		return offset;
	}
	
	self.getTotalPages = function(){
		var total_vehicles =self.vehicle_ids_list.length // Object.keys(self.vehicles).length;
		var total_pages = Math.ceil(total_vehicles/self.vehicles_limit) ;
		return total_pages;
	}

}


function VehicleWidget(){
	this.vehichle_id_control = null;
	this.vehicles = null
	this.dropdownobj = null;
	this.chosen=false;
	var self = this;
	self.vehicle_found_listener = []
	this.filters = {}
	this.vehicles = {}
	this.vin_number_control = null;
	this.after_intial_fill = null
	self.make_control = $("#make");
	self.year_control = $("#year");
	self.model_control = $("#model");
	self.vehicle_id_control = $("#vehicle_id");
//	self.dropdown_class = ".vehichle_selectbox"
	self.attachVehicleFound = function(fn){
		self.vehicle_found_listener.push(fn);
	}
	
	self.callVehicleFound = function(vehicles,from_vin){
		
		$.each(self.vehicle_found_listener,function(k,v){
			
			v(vehicles,from_vin)
		});
	}
	
	
	self.initialize = function(){
		self.setEventListeners();
		self.fillAll();
		
	}
	
	self.receiveOcr = function(text){
		if($.trim(text)!=""){
			$(self.vin_number_control).val(text);
			$(self.vin_number_control).trigger("blur")
		}else{
			BootstrapDialog.alert('Unable to process the VIN');
		}
		
	}
	
	self.setFilters = function(){
		self.filters = {}
		$(self.dropdownobj).each(function(k,v){
			var val = $.trim($(this).val());
			
			var drop_down  = $(this);
			if (val != ""){
				self.filters[drop_down.data("key")] = val
			}
		});
		return self.filters;
	}
	
	self.getFilters = function(){
		
		return self.filters;
	}
	
	self.filtered = function(other_vals){
		var retun = true;
		var filters = self.getFilters();
		
		$.each(filters,function(filter_k,filter_v){
			//if (filter_v != other_vals[filter_k+"__val"]){
			if (filter_v != other_vals[filter_k+"__id"]){
				retun =false
			}

		});
		
		return retun;
	}
	
	self.setInitials = function(){
		
		$(self.dropdownobj).each(function(k,v){
			var drop_down = $(this);
			if(drop_down.data("initial")!=""){
				var initial  = drop_down.data("initial")
				initial = $.trim(initial)
				drop_down.val(initial);
				drop_down.trigger("change");
			}
		});
		
	}
	
	self.fillAll = function(){
		var vehicles_available = {};
		self.setFilters();
		$(self.dropdownobj).each(function(k,v){
						var drop_down = $(this);
						self.clearControl(drop_down,drop_down.data("name"))
						$.each((self.vehicles),function(vehicle_key,vehicle_value){
							var key_dropdown =drop_down.data("key");
							if ( typeof self.vehicles[vehicle_key][key_dropdown+"__name"] !="undefined"  ){
								if(self.filtered(self.vehicles[vehicle_key])==true){
									self.appendUniqueValues(drop_down,self.vehicles[vehicle_key][key_dropdown+"__id"],self.vehicles[vehicle_key][key_dropdown+"__name"]);
									vehicles_available[self.vehicles[vehicle_key]["id"]] = self.vehicles[vehicle_key]
								}
							}
						});	
						self.sortDropDown (drop_down)
			});
	
		if(self.after_intial_fill!=null){
			self.after_intial_fill()
		}else{
			self.setInitials();
		}
		if(self.chosen==true){
			$(self.dropdownobj).chosen()
		}
		console.info("gettning here")
//		self.callVehicleFound(vehicles_available);
	}
	
	self.fillAllChange = function(current_obj){
			
			var vehicles_available = {};
			self.setFilters();
			$(self.dropdownobj).each(function(k,v){
				if (typeof current_obj == "undefined" ||
						current_obj.attr("id") != $(this).attr("id") ||
						current_obj.val()=="") {
							var drop_down = $(this);
							var old_val = $(this).val();
							self.clearControl(drop_down,drop_down.data("name"))
							$.each((self.vehicles),function(vehicle_key,vehicle_value){
								var key_dropdown =drop_down.data("key");
								if ( typeof self.vehicles[vehicle_key][key_dropdown+"__name"] !="undefined"  ){
									if(self.filtered(self.vehicles[vehicle_key])==true){
										self.appendUniqueValues(drop_down,self.vehicles[vehicle_key][key_dropdown+"__id"],self.vehicles[vehicle_key][key_dropdown+"__name"]);
										vehicles_available[self.vehicles[vehicle_key]["id"]] = self.vehicles[vehicle_key]
									}
								}
							});
							self.sortDropDown (drop_down)
							drop_down.val(old_val);
						}
				});
			self.callVehicleFound(vehicles_available);
			if(self.chosen){
				$(self.dropdownobj).trigger("chosen:updated");
			}
	}
	
	self.sortDropDown = function(dropdown){
		
		if(dropdown.attr("id")==self.year_control.attr("id")){
			self.sortOppositeDropDown(dropdown)
		}else{
				var selectList = dropdown.find("option");		
				selectList.sort(function(a,b){
						if($.trim($(a).val())!=""){
							a = a.innerHTML.toLowerCase();
							b = b.innerHTML.toLowerCase();
							if(a > b){
								return 1;
							}
		//					return a-b;
						}
						return -1
				});
				
				dropdown.html(selectList);
				dropdown.val("")
		}
	}
	self.sortOppositeDropDown = function(dropdown){

		
		var selectList = dropdown.find("option");		
		selectList.sort(function(a,b){
				if($.trim($(a).val())!=""){
					a = a.innerHTML.toLowerCase();
					b = b.innerHTML.toLowerCase();
					if(a < b){
						return 1;
					}
//					return a-b;
				}
				return -1
		});
		
		dropdown.html(selectList);
		dropdown.val("")
	}
	self.appendUniqueValues=function(control,value,text){
		
		if (self.valExists(control,value)==false){
			var option = $("<option>");
			option.val(value);
			option.text(text);
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
//		self.make_control.prop("disabled","disabled");
//		self.model_control.prop("disabled","disabled");
//		self.year_control.prop("disabled","disabled");
//		self.trim_control.prop("disabled","disabled");		
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
		self.model_control.remoeProp("disabled");
		self.year_control.remoeProp("disabled");

	}
	
	
	self.setEventListeners = function(){
		
		$(self.dropdownobj).change(function(){
			
			self.fillAllChange($(this));
		});
	
		if (self.vin_number_control !=null){
			$(self.vin_number_control).blur(function(){
				
				var make_index= 0;
				var model_index= 2;
				var year_index= 3;
				var vin_number = $.trim($(this).val());
				if(vin_number!=""){
					var make_from_vin =vin_number.charAt(make_index);
					var model_from_vin =vin_number.charAt(model_index);
					var year_from_vin =vin_number.charAt(year_index);
					
					$.each(self.vehicles,function(vehicle_key,vehicle_value){
						if(make_from_vin ==vehicle_value["make__val"] && model_from_vin ==vehicle_value["model__val"] && 
								year_from_vin == vehicle_value["year__val"]){
								self.make_control.val(vehicle_value["make__val"]);
								self.model_control.val(vehicle_value["model__val"]);
								self.year_control.val(vehicle_value["year__val"]);
								self.vehicle_id_control.val(vehicle_value["id"]);
								self.callVehicleFound([vehicle_value],true); //calling the vehicle found listeneres
						}
					});
				}
			});
		}
	}
	

			
	
}