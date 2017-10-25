$(document).ready(function(){
	/*$("ul").click(function (event) {
        alert("clicked: " + event.target.nodeName);
    });*/
	$('#bar').colorpicker();
	$('.editcolor').colorpicker();
    $("#FlagItemSearchField").hide();

    $('.list-group-item').each(function() {
    	$("#"+$(this).attr('id')).on("click", function () {
    		var value = $(this).attr('value');
            var res = value.replace(/\'/g, "\"");
            var ab = JSON.parse(res);
            loadFlagItems(ab);
            addShowEvents();
        });
	});
    

    function addShowEvents() {
        $("#FlagItemSearchField").show();
        $("#FlagItemSearchField").trigger("focus");
    }

    function loadFlagItems(ItemsArray) {
        $("#FlagItemSearchField").autocomplete({
            source: ItemsArray,
            minLength: 0,
            select: function (event, ui) {
                $("#FlagItemSearchField").autocomplete('search', $(this).val());
                $("#FlagItemSearchField").focus();
                // alert($("ul").children().length);
                // alert(event.currentTarget.children().length);
                return false;
            },
            close: function (event, ui) {
            	if ($('#FlagItemSearchField').val() == ""){
            		$("#FlagItemSearchField").hide();
            		 $(".list-group a").removeClass("active");
            	}
            	else{
                    $("#FlagItemSearchField").autocomplete('search', $(this).val());
                    $("#FlagItemSearchField").focus();
            	}
                return false;
            }
        }).focus(function (event, ui) {
            $(this).autocomplete('search', $(this).val())
        }).autocomplete("instance")._renderItem = function (ul, item) {
            return $("<li class='FlagListItems clearfix'>")
                .append("<a class='ItemLabel' title='Double Click to Edit' data-toggle='modal' data-target='.editflags"+item.value+"'>" + item.label + "</a><a class='DeleteItem'><span aria-hidden='true' id='DeleteFlag' title='Delete' class='DeleteFlageItem glyphicon glyphicon-remove-sign pull-right text-danger' value='"+item.value+"'></span></a>")
                .appendTo(ul.addClass('FlagItemsList'));
        };
    }
				var MyTimeField = function(config) {
			    jsGrid.Field.call(this, config);
			};
			 
			MyTimeField.prototype = new jsGrid.Field({
			 
			    css: "time-field",            // redefine general property 'css'
			    align: "center",              // redefine general property 'align'
			 
			         // custom property
			 
			    sorter: function(date1, date2) {
			        return "";
			    },
			 
			    itemTemplate: function(value) {
			        return value;
			    },
			 
			    insertTemplate: function(value) {
			        return this._insertPicker = $("<input>").timepicker();
			    },
			 
			    editTemplate: function(value) {
			        return this._editPicker = $("<input>").timepicker().timepicker("setTime",value);
			    },
			 
			    insertValue: function() {
			        return this._insertPicker.val().toString();
			    },
			 
			    editValue: function() {
			    	console.log(this._editPicker.val())
			        return this._editPicker.val().toString();
			    }
			});
			 
			jsGrid.fields.time = MyTimeField;
			


		    var MyDateField = function(config) {
		        jsGrid.Field.call(this, config);
		    };
		     
		    MyDateField.prototype = new jsGrid.Field({
		     
		        css: "date-field",            // redefine general property 'css'
		        align: "center",              // redefine general property 'align'
		     
		     
		        sorter: function(date1, date2) {
		            return "";
		        },
		     
		        itemTemplate: function(value) {
		            return new Date(value).toDateString();
		        },
		     
		        insertTemplate: function(value) {
		            return this._insertPicker = $("<input>").datepicker({ defaultDate: new Date() ,format: 'dd/mm/yyyy'});
		        },
		     
		        editTemplate: function(value) {
		            return this._editPicker = $("<input>").datepicker({format: 'dd/mm/yyyy'}).datepicker("setDate", new Date(value));
		        },
		     
		        insertValue: function() {
		            return this._insertPicker.datepicker("getDate",{format: 'dd/mm/yyyy'}).toISOString();
		        },
		     
		        editValue: function() {
		            return this._editPicker.datepicker("getDate",{format: 'dd/mm/yyyy'}).toISOString();
		        }
		    });
		     
		    jsGrid.fields.date = MyDateField;



            $("#resourcegrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete This Resource",
                controller: db,
                fields: [
                    { name: "Name", type: "text", width: 385, validate: "required" },
                    { name: "Rank", type: "number", width: 164 },
                    { name: "URL", type: "text", width: 604, validate: "required"  },
                    { type: "control",width: 135 }
                ]
            });
            $("#maincontactgrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete Contact",
                controller: shopcontacts,
                fields: [
                    { name: "Name", type: "text", width: 130, validate: "required" },
                    { name: "Email", type: "text", width: 130, validate: { message: "Please Enter Valid Email Address.", validator: function(value){
                    	var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                        return re.test(value);
                        }}  
                    },
                    { name: "Phone-WK", type: "text", width: 130, validate: { message: "Please Enter Valid Phone Number. Up to 10 digits allowed.", validator: function(value){
                    		var stripped = value.replace(/[\(\)\.\-\ ]/g, '');    
                    		if (value == "") {
                    			return false;
                         
                    		} else if (isNaN(parseInt(stripped))) {
                    			return false;
                    		} else if (!(stripped.length <= 10)) {
		                         return false;
                    		}
                    		return true; }}  
                    },
                    { name: "Phone-Cell", type: "text", width: 130, validate: { message: "Please Enter Valid Phone Number. Up to 10 digits allowed.", validator: function(value){
                		var stripped = value.replace(/[\(\)\.\-\ ]/g, '');    
                		if (value) {
                			if (isNaN(parseInt(stripped))) {
                    			return false;
                    		} else if (!(stripped.length <= 10)) {
    	                         return false;
                    		}
                     
                		}
                		return true; }} 
                    },
                    { type: "control",width: 55 }
                ]
            });
            $("#memailgrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete This Email ",
                controller: marketing,
                fields: [
                    { name: "Email", type: "text", width: 473, validate:{ message: "Please Enter Valid Email Address.", validator: function(value){
                    	var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                        return re.test(value);
                        }}  
                    },
                    { type: "control",width: 100 }
                ]
            });
            $("#femailgrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete This Email",
                controller: feedback,
                fields: [
                    { name: "Email", type: "text", width: 473, validate:{ message: "Please Enter Valid Email Address.", validator: function(value){
                    	var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                        return re.test(value);
                        }}  
                    },
                    { type: "control",width: 100 }
                ]
            });
            $("#semailgrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete This Email",
                controller: serviceemail,
                fields: [
                    { name: "Email", type: "text", width: 473, validate:{ message: "Please Enter Valid Email Address.", validator: function(value){
                    	var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                        return re.test(value);
                        }}  
                    },
                    { type: "control",width: 100 }
                ]
            });
            $("#smsgrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete This Number?",
                controller: sms,
                fields: [
                    { name: "SMS-Number", type: "text", width: 473, validate: { message: "Please Enter Valid Phone Number. Up to 10 digits allowed.", validator: function(value){
                		var stripped = value.replace(/[\(\)\.\-\ ]/g, '');    
                		if (value == "") {
                			return false;
                     
                		} else if (isNaN(parseInt(stripped))) {
                			return false;
                		} else if (!(stripped.length <= 10)) {
	                         return false;
                		}
                		return true; }} },
                    { type: "control",width: 100 }
                ]
            });
            $("#shophrsgrid").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete Shop Hr",
                controller: shophrs,
                fields: [
                    { name: "Day", type: "select",items: shophrs.days,valueField: "Id", textField: "Name", width: 168, validate: "required" },
                    { name: "From", type: "time", width: 168 },
                    { name: "To", type: "time", width: 168, validate: "required"  },
                    { type: "control",width: 71 }
                ]
            });
            $("#holidays").jsGrid({
                height: "100%",
                width: "100%",
                editing: true,
                inserting: true,
                sorting: true,
                autoload: true,
                deleteConfirm: "Are You Sure You Want To Delete Holiday",
                controller: holiday,
                onItemInserted: function(args){
                	console.log(args);
                },
                fields: [
                    { name: "Description", type: "text", width: 237, validate: "required" },
                    { name: "Date", type: "date", width: 237 },
                    { type: "control",width: 100 }
                ]
            });
        });

$(document).on('change','#new_image',function () {
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = imageIsLoadednew;
        reader.readAsDataURL(this.files[0]);
    }
});
function imageIsLoadednew(e) {
    $('#advimg').attr('src', e.target.result);
};
$('#contact_details').submit(function(e){
	$('#loading_page').show();
	var data = new FormData($(this).get(0));
	console.log(data);
	$.ajax({
	    url: url_details,
	    type: "POST",
	    data: data,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) {    
	    	$('#loading_page').hide();
	    	$('.sdtlmsg').html("Details Saved Successfully");
	    	$('.dtlss').show();
	    	$('.dtlss').fadeOut(10000);
	    },
	    error: function(data){
			$('#loading_page').hide();
			$('.edtlmsg').html("Error Occured While Saving Details");
	    	$('.dtlee').show();
	    	$('.dtlee').fadeOut(10000);
		}
	});
	e.preventDefault();
});

$("[data-hide]").on("click", function(){
    $(this).closest("." + $(this).attr("data-hide")).hide();
    return false;
});

$('input[type=checkbox]').click(function(){      
	$('#loading_page').show();
    if($(this).is(':not(:checked)')) {
    	$.post(url_delete_amenities,{'id':this.id},function(data){
    		$('#loading_page').hide();
	    }).fail(function(){
	    	$('#loading_page').hide();
	    }); 
    } 
    else{
    	$('#loading_page').show();
    	$.post(url_add_amenities,{'id':this.id},function(data){
    		$('#loading_page').hide();
	    }).fail(function(){
	    	$('#loading_page').hide();
	    });
    }
}); 
$(document).on('click','.veditadvisor',function(){
	$('#loading_page').show();
	$.post(get_editviewuaform,{'id': $(this).attr('id')},function(data){
	      $('.EDITADVISORS').html(data);
	      $.fn.editable.defaults.mode = 'inline';
			$('.ecM').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.ecT').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.ecW').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.ecTh').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.ecF').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.ecS').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.er_type').editable();
			$('.er_sdate').editable({
				viewformat: 'DD/MM/YYYY',
				combodate: {
				minYear: 2000,
				maxYear: 2020,
				}
			});
			$('.er_days').editable({
		        value: [7],    
		        source: [
		              {value: 1, text: 'Mon'},
		              {value: 2, text: 'Tue'},
		              {value: 3, text: 'Wed'},
		              {value: 4, text: 'Thur'},
		              {value: 5, text: 'Fri'},
		              {value: 6, text: 'Sat'},
		              {value: 7, text: 'Daily'},
		           ],
	           display: function(value, sourceData) {
	        	    //display checklist as comma-separated values
	        	    var html = [],
	        	      checked = $.fn.editableutils.itemsByValue(value, sourceData);

	        	    if (checked.length) {
	        	      $.each(checked, function(i, v) {
	        	        html.push($.fn.editableutils.escape(v.text));
	        	      });
	        	      $(this).html(html.join(', '));
	        	    } else {
	        	      $(this).empty();
	        	    }
	        	  }
		    });
			$('.er_stime').editable();
			$('.er_etime').editable();
			$('.er_repeat').editable({
				 value: 1,    
		        source: [
		              {value: 1, text: 'Yes'},
		              {value: 0, text: 'No'},
		           ]
			});
			$('.er_edate').editable({
				emptytext: 'Never',
				viewformat: 'DD/MM/YYYY',
				combodate: {
				minYear: 2000,
				maxYear: 2020,
				}
			});
	      $('.uta').addClass("hidden")
	  	  $('#viewedit').removeClass("hidden")
	  	  $('#loading_page').hide();
    }).fail(function(){
    	$('.eutamsg').html("Error Occured While Loading User Advisor Form");
		$('.euta').show();
		$('#loading_page').hide();
		$('.euta').fadeOut(10000);
    });
	return false
});
$(document).on('click','.cancleadv',function(){
	$('#viewedit').addClass("hidden")
	$('.uta').removeClass("hidden")
});
$(document).on('click','.veditteam',function(){
	$.post(edit_team,{'id': $(this).attr('id')},function(data){
		$('.uta').addClass("hidden")
		$( ".EDITTEAM" ).html( data );
		$('#addeditteam').removeClass("hidden")
	});
	
	return false
});
$(document).on('click','.vnewteam',function(){
	$('#loading_page').show();
	$('.uta').addClass("hidden")
	$('#addteam').removeClass("hidden")
	$('#loading_page').hide();
	return false
});
$(document).on('click','.cancelteam',function(){
	$('#loading_page').show();
	$('#addeditteam').addClass("hidden")
	$('.uta').removeClass("hidden")
	$('#loading_page').hide();
	return false
});
$(document).on('click','.canceladdteam',function(){
	$('#loading_page').show();
	$('#addteam').addClass("hidden")
	$('.uta').removeClass("hidden")
	$('#loading_page').hide();
	return false
});
$(document).on('click','.addud',function(){
	$('#loading_page').show();
	$.get( get_ua_form, function( data ) {
		  $( ".ADDUSERADVISOR" ).html( data );
		  $.fn.editable.defaults.mode = 'inline';
			$('.cM').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.cT').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.cW').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.cTh').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.cF').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.cS').editable({
		        value: 1,    
		        source: [
		              {value: 1, text: 'Available'},
		              {value: 0, text: 'UnAvailable'},
		           ]
		    });
			$('.r_type').editable();
			$('.r_sdate').editable({
				viewformat: 'DD/MM/YYYY',
				combodate: {
				minYear: 2000,
				maxYear: 2020,
				}
			});
			$('.r_days').editable({
		        value: [7],    
		        source: [
		              {value: 1, text: 'Mon'},
		              {value: 2, text: 'Tue'},
		              {value: 3, text: 'Wed'},
		              {value: 4, text: 'Thur'},
		              {value: 5, text: 'Fri'},
		              {value: 6, text: 'Sat'},
		              {value: 7, text: 'Daily'},
		           ],
	           display: function(value, sourceData) {
	        	    //display checklist as comma-separated values
	        	    var html = [],
	        	      checked = $.fn.editableutils.itemsByValue(value, sourceData);

	        	    if (checked.length) {
	        	      $.each(checked, function(i, v) {
	        	        html.push($.fn.editableutils.escape(v.text));
	        	      });
	        	      $(this).html(html.join(', '));
	        	    } else {
	        	      $(this).empty();
	        	    }
	        	  }
		    });
			$('.r_stime').editable();
			$('.r_etime').editable();
			$('.r_repeat').editable({
				 value: 1,    
		        source: [
		              {value: 1, text: 'Yes'},
		              {value: 0, text: 'No'},
		           ]
			});
			$('.r_edate').editable({
				emptytext: 'Never',
				viewformat: 'DD/MM/YYYY',
				combodate: {
				minYear: 2000,
				maxYear: 2020,
				}
			});
		  $('.uta').addClass("hidden")
		  $('#adduseradvisor').removeClass("hidden")
		  $('#loading_page').hide();
	}).fail(function(){
		$('.eutamsg').html("Error Occured While Loading User Advisor Form");
		$('.euta').show();
		$('#loading_page').hide();
		$('.euta').fadeOut(10000);
	});
	return false
});

$(document).on('click','.cancelud',function(){
	$('#loading_page').show();
	$('#adduseradvisor').addClass("hidden")
	$('.uta').removeClass("hidden")
	$('#loading_page').hide();
	return false
});

$(document).on('submit','#new_user_advisor_form',function(e){
	$('#loading_page').show();
	var formData =  new FormData($(this).get(0));
	var cap = {};
	$("#capacitytable tbody td").each(function(){
		if($(this).attr('id')){
			cap[$(this).attr('id')] = $('.'+ $(this).attr('id')).editable("getValue").undefined;
		}
	})
	rest_Arr = [];
	$("#restriction_table tbody tr").each(function(){
		var res = {};
		$(this).find('td').each(function(){
			if($(this).attr('id')){
				res[$(this).attr('id')] = $(this).find('a.' + $(this).attr('id')).editable("getValue").undefined;
			}
        });
		rest_Arr.push(res);
	})
	console.log(rest_Arr);
	cap = JSON.stringify(cap);
	rest_Arr = JSON.stringify(rest_Arr);
	formData.append('capacity',cap);
	formData.append('restrictions' , rest_Arr);
	console.log(formData);
	console.log(cap);
	$.ajax({
	    url: add_user_advisor,
	    type: "POST",
	    data: formData,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) {
	    	$('#adduseradvisor').addClass("hidden");
	    	$('#MAINUAT').html(data);
	    	$('.uta').removeClass("hidden");
//	    	$('.sutamsg').html("New Advisor User Saved Successfully");
//			$('.suta').show();
			$('#loading_page').hide();
			$('.suta').fadeOut(10000);
	    	
	    },
	    error : function(data){
	    	$('#adduseradvisor').addClass("hidden");
	    	$('.uta').removeClass("hidden");
	    	$('.eutamsg').html("Error Occured While Saving User Advisor");
			$('.euta').show();
			$('#loading_page').hide();
			$('.euta').fadeOut(10000);
	    }
	});
	e.preventDefault();
});

$(document).on('click','#add_restriction',function(){
	$('#loading_page').show();
	$('#restriction_table tbody').append('<tr><td id="r_type"><a href="#" class="r_type" data-type="text"></a></td> <td id="r_sdate"><a href="#" class="r_sdate" data-type="combodate"></a></td><td id="r_days"><a href="#" class="r_days" data-type="checklist"></a></td> <td id="r_stime"><a href="#" class="r_stime" data-type="combodate" data-template="hh:mm a" data-format="hh:mm a" data-viewformat="hh:mm a"></a></td><td id="r_etime"><a href="#" class="r_etime" data-type="combodate" data-template="hh:mm a" data-format="hh:mm a" data-viewformat="hh:mm a"></a></td> <td id="r_repeat"><a href="#" class="r_repeat" data-type="select"></a></td><td id="r_edate"><a href="#" class="r_edate" data-type="combodate"></a></td> <td><a href="#" id="del_rest"><span class="glyphicon glyphicon-minus"></span></a></td></tr>');
	$('.r_type').editable();
	$('.r_sdate').editable({
		viewformat: 'DD/MM/YYYY',
		combodate: {
		minYear: 2000,
		maxYear: 2020,
		}
	});
	$('.r_days').editable({
		inputclass: 'input-medium privacy-select',
        value: [7],    
        source: [
              {value: 1, text: 'Mon'},
              {value: 2, text: 'Tue'},
              {value: 3, text: 'Wed'},
              {value: 4, text: 'Thur'},
              {value: 5, text: 'Fri'},
              {value: 6, text: 'Sat'},
              {value: 7, text: 'Daily'},
           ],
       display: function(value, sourceData) {
    	    //display checklist as comma-separated values
    	    var html = [],
    	      checked = $.fn.editableutils.itemsByValue(value, sourceData);

    	    if (checked.length) {
    	      $.each(checked, function(i, v) {
    	        html.push($.fn.editableutils.escape(v.text));
    	      });
    	      $(this).html(html.join(', '));
    	    } else {
    	      $(this).empty();
    	    }
    	  }
    });
	$('.r_stime').editable();
	$('.r_etime').editable();
	$('.r_repeat').editable({
		 value: 1,    
         source: [
              {value: 1, text: 'Yes'},
              {value: 0, text: 'No'},
           ]
	});
	$('.r_edate').editable({
		emptytext: 'Never',
		viewformat: 'DD/MM/YYYY',
		combodate: {
		minYear: 2000,
		maxYear: 2020,
		}
	});
	$('#loading_page').hide();
	return false
});
$(document).on('click','#del_rest',function(){
	$('#loading_page').show();
	$(this).closest('tr').remove();
	$('#loading_page').hide();
	return false
});

$(document).on('click','#edit_restriction',function(){
	$('#loading_page').show();
	$('#edit_restriction_table tbody').append('<tr id=""><td id="er_type"><a href="#" class="er_type" data-type="text" ></a></td> <td id="er_sdate"><a href="#" class="er_sdate" data-type="combodate" ></a></td><td id="er_days"><a href="#" class="er_days" data-type="checklist"></a></td> <td id="er_stime"><a href="#" class="er_stime" data-type="combodate" data-template="hh:mm a" data-format="hh:mm a" data-viewformat="hh:mm a"></a></td><td id="er_etime"><a href="#" class="er_etime" data-type="combodate" data-template="hh:mm a" data-format="hh:mm a" data-viewformat="hh:mm a"></a></td> <td id="er_repeat"><a href="#" class="er_repeat" data-type="select"></a></td><td id="er_edate"><a href="#" class="er_edate" data-type="combodate"></a></td> <td><a href="#" id="del_rest"><span class="glyphicon glyphicon-minus"></span></a></td></tr>');
	$('.er_type').editable();
	$('.er_sdate').editable({
		viewformat: 'DD/MM/YYYY',
		combodate: {
		minYear: 2000,
		maxYear: 2020,
		}
	});
	$('.er_days').editable({
		inputclass: 'input-medium privacy-select',
        value: [7],    
        source: [
              {value: 1, text: 'Mon'},
              {value: 2, text: 'Tue'},
              {value: 3, text: 'Wed'},
              {value: 4, text: 'Thur'},
              {value: 5, text: 'Fri'},
              {value: 6, text: 'Sat'},
              {value: 7, text: 'Daily'},
           ],
       display: function(value, sourceData) {
    	    //display checklist as comma-separated values
    	    var html = [],
    	      checked = $.fn.editableutils.itemsByValue(value, sourceData);

    	    if (checked.length) {
    	      $.each(checked, function(i, v) {
    	        html.push($.fn.editableutils.escape(v.text));
    	      });
    	      $(this).html(html.join(', '));
    	    } else {
    	      $(this).empty();
    	    }
    	  }
    });
	$('.er_stime').editable();
	$('.er_etime').editable();
	$('.er_repeat').editable({
		 value: 1,    
         source: [
              {value: 1, text: 'Yes'},
              {value: 0, text: 'No'},
           ]
	});
	$('.er_edate').editable({
		emptytext: 'Never',
		viewformat: 'DD/MM/YYYY',
		combodate: {
		minYear: 2000,
		maxYear: 2020,
		}
	});
	$('#loading_page').hide();
	return false
});
$(document).on('submit','#edit_user_advisor_form',function(e){
	$('#loading_page').show();
	var formData =  new FormData($(this).get(0));
	var cap = {};
	$("#edit_capacitytable tbody tr").each(function(){
		cap['id'] = $(this).attr('id');
		$(this).find('td').each(function(){
			if($(this).attr('id')){
				cap[$(this).attr('id')] = $('.'+ $(this).attr('id')).editable("getValue").undefined;
			}
		});
	});
	rest_Arr=[]
	$("#edit_restriction_table tbody tr").each(function(){
		rst ={}
		rst['id'] = $(this).attr('id');
		$(this).find('td').each(function(){
			if($(this).attr('id')){
				rst[$(this).attr('id')] = $(this).find('a.' + $(this).attr('id')).editable("getValue").undefined;
			}
		});
		rest_Arr.push(rst);
	});
	cap = JSON.stringify(cap);
	rest_Arr = JSON.stringify(rest_Arr);
	console.log(cap);
	console.log(rest_Arr)
	formData.append('capacity',cap);
	formData.append('restrictions' , rest_Arr);
	console.log(formData)
	$.ajax({
	    url: edit_user_advisor,
	    type: "POST",
	    data: formData,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) {
	    	$('#viewedit').addClass("hidden")
	    	$('#MAINUAT').html(data)
	    	$('.uta').removeClass("hidden")
//	    	$('.sutamsg').html("Advisor User Edits Saved Successfully");
//			$('.suta').show();
			$('#loading_page').hide();
//			$('.suta').fadeOut(10000);
	    },
	    error: function(data){
	    	$('.eutamsg').html("Error Occured While Saving Edits For Advisor Users");
			$('.euta').show();
			$('#loading_page').hide();
			$('.euta').fadeOut(10000);
	    }
	});
	e.preventDefault();
});

$(document).on('change','#edit_image',function () {
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = imageIsLoaded;
        reader.readAsDataURL(this.files[0]);
    }
});
function imageIsLoaded(e) {
    $('#editadvimg').attr('src', e.target.result);
};
$(document).on('click' , '.createteam',function(){
	$('#loading_page').show();
	if ($("input[name=team_name]").val()){
		$.post(add_team,{'name': $("input[name=team_name]").val() },function(data){
			$('#addteam').addClass("hidden")
			$('#MAINUAT').html(data)
			$('.uta').removeClass("hidden")
			$('.sutamsg').html("Team Added Successfully");
			$('.suta').show();
			$('#loading_page').hide();
			$('.suta').fadeOut(10000);
	    }).fail(function(data){
	    	$('#addteam').addClass("hidden")
			$('.uta').removeClass("hidden")
			$('.eutamsg').html("Error Occured While Adding Team");
			$('.euta').show();
			$('#loading_page').hide();
			$('.euta').fadeOut(10000);
	    });
	}
});
$(document).on('click', '.addteammember', function(){
	$('#loading_page').show();
	if ($("select[name=add_team_advisors]").val()){
		$.post(add_team_members,{'team_members': $("select[name=add_team_advisors]").val() , 'id' : $("input[name=team_id]").val() },function(data){
			$('.EDITTEAM').html(data)
			$('#addeditteam').removeClass("hidden")
			$('.sutamsg').html("Member Added Successfully");
			$('.suta').show();
			$('#loading_page').hide();
			$('.suta').fadeOut(10000);
		}).fail(function(){
			$('#addeditteam').removeClass("hidden")
			$('.eutamsg').html("Error Occured while Adding Member");
			$('.euta').show();
			$('#loading_page').hide();
			$('.euta').fadeOut(10000);
		});
	}
});
$(document).on('click','.deleteteammembers',function(){
	$('#loading_page').show();
	$.post(delete_team_members,{'team_mem_id': $(this).closest('tr').attr('id') , 'id' : $("input[name=team_id]").val() },function(data){
		$('.EDITTEAM').html(data)
		$('#addeditteam').removeClass("hidden")
		$('.sutamsg').html("Member Removed");
		$('.suta').show();
		$('#loading_page').hide();
		$('.suta').fadeOut(10000);
	}).fail(function(){
		$('#addeditteam').removeClass("hidden")
		$('.eutamsg').html("Error Occured While Removing Member");
		$('.euta').show();
		$('#loading_page').hide();
		$('.euta').fadeOut(10000);
	});
	return false
})
$(document).on('click','.removeteam' ,function(){
	$('#loading_page').show();
	$.post(remove_team,{'id': $(this).attr('id')},function(data){
		$('#MAINUAT').html(data)
		$('.sutamsg').html("Team Deleted Successfully");
		$('.suta').show();
		$('#loading_page').hide();
		$('.suta').fadeOut(10000);
    }).fail(function(){
    	$('.eutamsg').html("Error Occured While Deleting Team");
		$('.euta').show();
		$('#loading_page').hide();
		$('.euta').fadeOut(10000);
    });
	return false
});
$(document).on('click','.removeuseradvisor' ,function(){
	$('#loading_page').show();
	$.post(remove_user_advisor,{'id': $(this).attr('id')},function(data){
		$('#MAINUAT').html(data)
		$('.sutamsg').html("User Advisor Removed Successfully");
		$('.suta').show();
		$('#loading_page').hide();
		$('.suta').fadeOut(10000);
    }).fail(function(){
    	$('.eutamsg').html("Error Occured While Removing User Advisor");
		$('.euta').show();
		$('#loading_page').hide();
		$('.euta').fadeOut(10000);
    });
	return false
});
$(document).on('click','.cancle_new_user_advisor',function(){
	$('#adduseradvisor').addClass("hidden");;
	$('.uta').removeClass("hidden");
});
$(document).on('click', '.deleteadv' , function(){
	$('#loading_page').show();
	$.post(remove_user_advisor,{'id': $('#id_user_id').val()},function(data){
		$('#MAINUAT').html(data);
		$('.sutamsg').html("User Advisor Removed Successfully");
		$('#viewedit').addClass("hidden")
		$('.uta').removeClass("hidden")
		$('.suta').show();
		$('#loading_page').hide();
		$('.suta').fadeOut(10000);
    }).fail(function(){
    	$('.eutamsg').html("Error Occured While Removing User Advisor");
    	$('#viewedit').addClass("hidden")
    	$('.uta').removeClass("hidden")
		$('.euta').show();
		$('#loading_page').hide();
		$('.euta').fadeOut(10000);
    });
	return false
});
$(document).on('submit', '#add_package',function(e){
		$('.addnewpackage').modal('toggle');
		$('#loading_page').show();
		var data = new FormData($(this).get(0));
		console.log(data);
		$.ajax({
		    url: add_package,
		    type: "POST",
		    data: data,
		    cache: false,
		    processData: false,
		    contentType: false,
		    success: function(data) { 
				$('#inspmain').html(data);
				$('#id_pack_name').val("");
				$('.sinspmsg').html("Package Successfully Created");
				$('#loading_page').hide();
				$('.sinsp').show();
				$('.sinsp').fadeOut(10000);
		    },
		    error: function(){
			$('#id_pack_name').val("");
			$('.einspmsg').html("Error Occured While Creating Package");
			$('.einsp').show();
			$('#loading_page').hide();
			$('.einsp').fadeOut(10000);
		    }
		});
		e.preventDefault();
});

$(document).on("submit", "#add_category",function(e){
	$('.addnewcategory').modal('toggle');
	$('#loading_page').show();
	var data = new FormData($(this).get(0));
	console.log(data);
	$.ajax({
	    url: add_category,
	    type: "POST",
	    data: data,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) { 
			$('#id_cat_name').val("");
			var c_id = data['cat_id'];
			$.post(get_category,{'id': data['pack_id']},function(data){
				$('.catlist').html(data);
				$("#cattlist").val(c_id);
		    }).fail(function(){
		    	$('#loading_page').hide();
				$('.einspmsg').html("Error Occured While Getting Category");
				$('.einsp').show();
				$('#loading_page').hide();
				$('.einsp').fadeOut(10000);
		    });
			$.post(get_insp_items,{'id': data['cat_id']},function(data){
				$('#insp_detail').html(data);
		    }).fail(function(){
				$('.einspmsg').html("Error Occured While Getting Inspection Items");
				$('.einsp').show();
				$('#loading_page').hide();
				$('.einsp').fadeOut(10000);
		    });
			$("#packagelistitems").val(data['pack_id']);
			$('.sinspmsg').html("Category Successfully Created");
			$('.sinsp').show();
			$('#loading_page').hide();
			$('.sinsp').fadeOut(10000);
	    },
	    error: function(){
		$('#id_cat_name').val("")
		$('.einspmsg').html("Error Occured While Creating Category");
		$('.einsp').show();
		$('#loading_page').hide();
		$('.einsp').fadeOut(10000);
	    }
	});
	e.preventDefault();
});

$(document).on('change','#packagelistitems',function(){
	$('#insp_detail').html("");
	if ($('#packagelistitems').val()){
		$('#loading_page').show();
		$.post(get_category,{'id': $('#packagelistitems').val()},function(data){
			$('.catlist').html(data);
			$('#loading_page').hide();
	    }).fail(function(){
	    	$('#loading_page').hide();
			$('.einspmsg').html("Error Occured While Getting Category");
			$('.einsp').show();
			$('#loading_page').hide();
			$('.einsp').fadeOut(10000);
	    });
	}
	return false
});

$(document).on('change','.categorylist',function(){
	if ($('.categorylist').val()){
		$('#loading_page').show();
		$.post(get_insp_items,{'id': $('.categorylist').val()},function(data){
			$('#insp_detail').html(data);
			$('#loading_page').hide();
	    }).fail(function(){
			$('.einspmsg').html("Error Occured While Getting Inspection Items");
			$('.einsp').show();
			$('#loading_page').hide();
			$('.einsp').fadeOut(10000);
	    });
	}else{
		$('#insp_detail').html("");
	}
	return false
});
$(document).on('click', '.addcatitems', function(){
	$('#loading_page').show();
	$.post(add_cat_items,{'cat_id': $('.categorylist').val() , 'items' : $('.itemslist').val()},function(data){
		$('#insp_detail').html(data);
		$('.sinspmsg').html("Items Successfully Added");
		$('.sinsp').show();
		$('#loading_page').hide();
		$('.sinsp').fadeOut(10000);
    }).fail(function(){
		$('.einspmsg').html("Error Occured While Adding Items");
		$('.einsp').show();
		$('#loading_page').hide();
		$('.einsp').fadeOut(10000);
    });
});

$(document).on('click', '.removecatitems', function(){
	$('#loading_page').show();
	$.post(remove_cat_items,{'cat_id': $('.categorylist').val() , 'items' : $('.catitemlist').val()},function(data){
		$('#insp_detail').html(data);
		$('.sinspmsg').html("Items Successfully Removed");
		$('.sinsp').show();
		$('#loading_page').hide();
		$('.sinsp').fadeOut(10000);
    }).fail(function(){
		$('.einspmsg').html("Error Occured While Removing Items");
		$('.einsp').show();
		$('#loading_page').hide();
		$('.einsp').fadeOut(10000);
    });
});

$(document).on('submit', '#additemnew',function(e){
	$('.addnewitem').modal('toggle');
	$('#loading_page').show();
	var data = new FormData($(this).get(0));
	data.append('cat_id' , $('.categorylist').val());
	console.log(data);
	$.ajax({
	    url: add_new_item,
	    type: "POST",
	    data: data,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) { 
	    	$('#insp_detail').html(data);
	    	$('#id_item_name').val("");
			$('.sinspmsg').html("Item Successfully Created");
			$('.sinsp').show();
			$('#loading_page').hide();
			$('.sinsp').fadeOut(10000);
	    },
	    error: function(){
		$('#id_item_name').val("");
		$('.einspmsg').html("Error Occured While Creating Item");
		$('.einsp').show();
		$('#loading_page').hide();
		$('.einsp').fadeOut(10000);
	    }
	});
	e.preventDefault();
});
$(document).on("click",".list-group a", function() {
    $(".list-group a").removeClass("active");
    $(this).addClass("active");
 });

$(document).on('submit','#editflagform',function(e){
	var data = new FormData($(this).get(0));
	$(".editflags"+data.get("eflagid")).modal('toggle');
	$('#loading_page').show();
	$.ajax({
	    url: edit_flag,
	    type: "POST",
	    data: data,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) { 
	    	$('#flagmain').html(data);
	    	$('#bar').colorpicker();
	    	$('.editcolor').colorpicker();
	    	$("#FlagItemSearchField").hide();
	        $('.list-group-item').each(function() {
	        	$("#"+$(this).attr('id')).on("click", function () {
	        		var value = $(this).attr('value');
	                var res = value.replace(/\'/g, "\"");
	                var ab = JSON.parse(res);
	                loadFlagItems(ab);
	                addShowEvents();
	            });
	    	});
	        

	        function addShowEvents() {
	            $("#FlagItemSearchField").show();
	            $("#FlagItemSearchField").trigger("focus");
	        }

	        function loadFlagItems(ItemsArray) {
	            $("#FlagItemSearchField").autocomplete({
	                source: ItemsArray,
	                minLength: 0,
	                select: function (event, ui) {
	                    $("#FlagItemSearchField").autocomplete('search', $(this).val());
	                    $("#FlagItemSearchField").focus();
	                    // alert($("ul").children().length);
	                    // alert(event.currentTarget.children().length);
	                    return false;
	                },
	                close: function (event, ui) {
	                	if ($('#FlagItemSearchField').val() == ""){
	                		$("#FlagItemSearchField").hide();
	                		 $(".list-group a").removeClass("active");
	                	}
	                	else{
	                        $("#FlagItemSearchField").autocomplete('search', $(this).val());
	                        $("#FlagItemSearchField").focus();
	                	}
	                    return false;
	                }
	            }).focus(function (event, ui) {
	                $(this).autocomplete('search', $(this).val())
	            }).autocomplete("instance")._renderItem = function (ul, item) {
	                return $("<li class='FlagListItems clearfix'>")
	                    .append("<a class='ItemLabel' title='Double Click to Edit' data-toggle='modal' data-target='.editflags"+item.value+"'>" + item.label + "</a><a class='DeleteItem'><span aria-hidden='true' id='DeleteFlag' title='Delete' class='DeleteFlageItem glyphicon glyphicon-remove-sign pull-right text-danger' value='"+item.value+"'></span></a>")
	                    .appendTo(ul.addClass('FlagItemsList'));
	            };
	        }
	    	$('.sflagmsg').html("Flag Successfully Edit");
			$('.sflag').show();
			$('#loading_page').hide();
			$('.sflag').fadeOut(20000);
			
	    },
	    error: function(){
	    	$('.eflagmsg').html("Error Occured While Flag Edit");
			$('.eflag').show();
			$('#loading_page').hide();
			$('.eflag').fadeOut(20000);
	    }
	});
	e.preventDefault();
});
$(document).on('submit','#addnewflag',function(e){
	var data = new FormData($(this).get(0));
	$(".addflag").modal('toggle');
	$('#loading_page').show();
	$.ajax({
	    url: add_flag,
	    type: "POST",
	    data: data,
	    cache: false,
	    processData: false,
	    contentType: false,
	    success: function(data) { 
	    	$('#flagmain').html(data);
	    	$('#bar').colorpicker();
	    	$('.editcolor').colorpicker();
	    	$("#FlagItemSearchField").hide();
	        $('.list-group-item').each(function() {
	        	$("#"+$(this).attr('id')).on("click", function () {
	        		var value = $(this).attr('value');
	                var res = value.replace(/\'/g, "\"");
	                var ab = JSON.parse(res);
	                loadFlagItems(ab);
	                addShowEvents();
	            });
	    	});
	        

	        function addShowEvents() {
	            $("#FlagItemSearchField").show();
	            $("#FlagItemSearchField").trigger("focus");
	        }

	        function loadFlagItems(ItemsArray) {
	            $("#FlagItemSearchField").autocomplete({
	                source: ItemsArray,
	                minLength: 0,
	                select: function (event, ui) {
	                    $("#FlagItemSearchField").autocomplete('search', $(this).val());
	                    $("#FlagItemSearchField").focus();
	                    // alert($("ul").children().length);
	                    // alert(event.currentTarget.children().length);
	                    return false;
	                },
	                close: function (event, ui) {
	                	if ($('#FlagItemSearchField').val() == ""){
	                		$("#FlagItemSearchField").hide();
	                		 $(".list-group a").removeClass("active");
	                	}
	                	else{
	                        $("#FlagItemSearchField").autocomplete('search', $(this).val());
	                        $("#FlagItemSearchField").focus();
	                	}
	                    return false;
	                }
	            }).focus(function (event, ui) {
	                $(this).autocomplete('search', $(this).val())
	            }).autocomplete("instance")._renderItem = function (ul, item) {
	                return $("<li class='FlagListItems clearfix'>")
	                    .append("<a class='ItemLabel' title='Double Click to Edit' data-toggle='modal' data-target='.editflags"+item.value+"'>" + item.label + "</a><a class='DeleteItem'><span aria-hidden='true' id='DeleteFlag' title='Delete' class='DeleteFlageItem glyphicon glyphicon-remove-sign pull-right text-danger' value='"+item.value+"'></span></a>")
	                    .appendTo(ul.addClass('FlagItemsList'));
	            };
	        }
	    	$('.sflagmsg').html("Flag Successfully Added");
			$('.sflag').show();
			$('#loading_page').hide();
			$('.sflag').fadeOut(20000);
			
	    },
	    error: function(){
	    	$('.eflagmsg').html("Error Occured While Adding Flag");
			$('.eflag').show();
			$('#loading_page').hide();
			$('.eflag').fadeOut(20000);
	    }
	});
	e.preventDefault();
});

$(document).on("click","#DeleteFlag",function(){
	$('#loading_page').show();
	$.post(del_flag,{'id': $(this).attr('value')},function(data){
		$('#flagmain').html(data);
		$('#bar').colorpicker();
		$('.editcolor').colorpicker();
    	$("#FlagItemSearchField").hide();
        $('.list-group-item').each(function() {
        	$("#"+$(this).attr('id')).on("click", function () {
        		var value = $(this).attr('value');
                var res = value.replace(/\'/g, "\"");
                var ab = JSON.parse(res);
                loadFlagItems(ab);
                addShowEvents();
            });
    	});
        

        function addShowEvents() {
            $("#FlagItemSearchField").show();
            $("#FlagItemSearchField").trigger("focus");
        }

        function loadFlagItems(ItemsArray) {
            $("#FlagItemSearchField").autocomplete({
                source: ItemsArray,
                minLength: 0,
                select: function (event, ui) {
                    $("#FlagItemSearchField").autocomplete('search', $(this).val());
                    $("#FlagItemSearchField").focus();
                    // alert($("ul").children().length);
                    // alert(event.currentTarget.children().length);
                    return false;
                },
                close: function (event, ui) {
                	if ($('#FlagItemSearchField').val() == ""){
                		$("#FlagItemSearchField").hide();
                		 $(".list-group a").removeClass("active");
                	}
                	else{
                        $("#FlagItemSearchField").autocomplete('search', $(this).val());
                        $("#FlagItemSearchField").focus();
                	}
                    return false;
                }
            }).focus(function (event, ui) {
                $(this).autocomplete('search', $(this).val())
            }).autocomplete("instance")._renderItem = function (ul, item) {
                return $("<li class='FlagListItems clearfix'>")
                    .append("<a class='ItemLabel' title='Double Click to Edit' data-toggle='modal' data-target='.editflags"+item.value+"'>" + item.label + "</a><a class='DeleteItem'><span aria-hidden='true' id='DeleteFlag' title='Delete' class='DeleteFlageItem glyphicon glyphicon-remove-sign pull-right text-danger' value='"+item.value+"'></span></a>")
                    .appendTo(ul.addClass('FlagItemsList'));
            };
        }
    	$('.sflagmsg').html("Flag Successfully Deleted");
		$('.sflag').show();
		$('#loading_page').hide();
		$('.sflag').fadeOut(10000);
    }).fail(function(){
    	$('.eflagmsg').html("Error Occured While Deleting Flag");
		$('.eflag').show();
		$('#loading_page').hide();
		$('.eflag').fadeOut(10000);
    });
});
$(document).on('change', '#id_edit_package', function(){
	if ($('#id_edit_package').val()){
		$('#loading_page').show();
		$.post(get_package_detail,{'id': $('#id_edit_package').val()},function(data){
			$('#editpack').html(data);
			$('#loading_page').hide();
	    }).fail(function(){
	    	$('#loading_page').hide();
	    });
	}
	return false
});
$(document).on('click', '.saveeditpack', function(){
	if ($('#id_edit_package').val()){
		$('#loading_page').show();
		$('.editpackage').modal('toggle');
		$.post(edit_package,{'pack_id': $('#id_edit_package').val() , 'pack_name' : $('#id_pack_edit_name').val()},function(data){
			$('#inspmain').html(data);
			$('.sinspmsg').html("Package Saved Successfully");
			$('#loading_page').hide();
			$('.sinsp').show();
			$('.sinsp').fadeOut(10000);
	    }).fail(function(){
	    	$('.einspmsg').html("Error Occured While Saving Package");
			$('#loading_page').hide();
			$('.einsp').show();
			$('.einsp').fadeOut(10000);
	    });
	}
	
});
$(document).on('click', '.deletepack', function(){
	if ($('#id_edit_package').val()){
		$('#loading_page').show();
		$('.editpackage').modal('toggle');
		$.post(delete_package,{'pack_id': $('#id_edit_package').val()},function(data){
			$('#inspmain').html(data);
			$('.sinspmsg').html("Package Deleted Successfully");
			$('#loading_page').hide();
			$('.sinsp').show();
			$('.sinsp').fadeOut(10000);
	    }).fail(function(){
	    	$('.einspmsg').html("Error Occured while Deleting Package");
			$('#loading_page').hide();
			$('.einsp').show();
			$('.einsp').fadeOut(10000);
	    });
	}
	
});

$(document).on('change', '#id_edit_cpackage', function(){
	if ($('#id_edit_cpackage').val()){
		$('#loading_page').show();
		$.post(get_edit_cat,{'id': $('#id_edit_cpackage').val()},function(data){
			$('#editcat').html(data);
			$('#loading_page').hide();
	    }).fail(function(){
	    	$('#loading_page').hide();
	    });
	}
	return false
});
$(document).on('change', '#id_edit_cat', function(){
	if ($('#id_edit_cat').val()){
		$('#id_cat_edit_name').val($('#id_edit_cat option:selected').text());
		$('.etcat').removeClass("hidden");
	}
	return false
});
$(document).on('click', '.saveeditcat', function(){
	if ($('#id_edit_cat').val()){
		$('#loading_page').show();
		$('.editcategory').modal('toggle');
		$.post(edit_cat,{'cat_id': $('#id_edit_cat').val() , 'cat_name' : $('#id_cat_edit_name').val()},function(data){
			$('#inspmain').html(data);
			$('.sinspmsg').html("Category Saved Successfully");
			$('#loading_page').hide();
			$('.sinsp').show();
			$('.sinsp').fadeOut(10000);
	    }).fail(function(){
	    	$('.einspmsg').html("Error Occured While Saving Category");
			$('#loading_page').hide();
			$('.einsp').show();
			$('.einsp').fadeOut(10000);
	    });
	}
	
});

$(document).on('click', '.deletecat', function(){
	if ($('#id_edit_cat').val()){
		$('#loading_page').show();
		$('.editcategory').modal('toggle');
		$.post(delete_cat,{'cat_id': $('#id_edit_cat').val()},function(data){
			$('#inspmain').html(data);
			$('.sinspmsg').html("Category Deleted Successfully");
			$('#loading_page').hide();
			$('.sinsp').show();
			$('.sinsp').fadeOut(10000);
	    }).fail(function(){
	    	$('.einspmsg').html("Error Occured while Deleting Category");
			$('#loading_page').hide();
			$('.einsp').show();
			$('.einsp').fadeOut(10000);
	    });
	}
	
});

$(document).on('click', '.deletecatitems', function(){
	$('#loading_page').show();
	$.post(delete_items,{'cat_id': $('.categorylist').val() , 'items' : $('.itemslist').val()},function(data){
		$('#insp_detail').html(data);
		$('.sinspmsg').html("Items Successfully Deleted");
		$('.sinsp').show();
		$('#loading_page').hide();
		$('.sinsp').fadeOut(10000);
    }).fail(function(){
		$('.einspmsg').html("Error Occured While Deleting Items");
		$('.einsp').show();
		$('#loading_page').hide();
		$('.einsp').fadeOut(10000);
    });
});