function Dealership() {
	var self = this;
	this.dateTimeValueMomentFormat = ""
	
	this.getCookie = function(name){
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	};	
	
	this.csrfSafeMethod =  function(method){
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	
	this.getTemplateFromServer = function(url, data, callback, callback_attr){
		$('#loading_page').show();	
		var csrftoken = self.getCookie('csrftoken');
		$.ajax({
			beforeSend: function(xhr, settings) {
		        if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    },		
	        url: url,
	        type: 'POST',
	        data: data,
	        accept : 'application/json',
	        success: function(content) {
	        	$('#loading_page').hide();
	        	if(callback !== undefined)
	        		callback(content, callback_attr);	
	        },error:function(){
	        	$("#loading_page").hide();
	        }
        });
	};
	
	this.getDataFromServer = function(url, data, callback, callback_attr){	
		$("#loading_page").show();
		var csrftoken = self.getCookie('csrftoken');
		$.ajax({
			beforeSend: function(xhr, settings) {
		        if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    },		
	        url: url,
	        type: 'POST',
	        data: data,
	        accept : 'application/json',
	        dataType: "json",
	        success: function(content) {
	        	if(callback !== undefined)
	        		callback(content, callback_attr);
	        	$("#loading_page").hide();
	        },error:function(){
	        	$("#loading_page").hide();
	        }
        });
	};
	
	this.createupdatesr = function(url, data, callback, callback_attr){
		$("#loading_page").show();
		var csrftoken = self.getCookie('csrftoken');
		data.append('csrfmiddlewaretoken', csrftoken);
		$.ajax({
		    url: url,
		    type: "POST",
		    data: data,
		    accept : 'application/json',
	        dataType: "json",
		    cache: false,
		    processData: false,
		    contentType: false,
		    success: function(content) {    
		    	if(callback !== undefined)
	        		callback(content, callback_attr);
		    	$('#loading_page').hide();
		    },
		    error: function(data){
		    	$("#loading_page").hide();
			}
		});
	};
	this.getGetDataFromServer = function(url, data, callback, callback_attr){	
		$("#loading_page").show();
		var csrftoken = self.getCookie('csrftoken');
		$.ajax({
			beforeSend: function(xhr, settings) {
		        if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    },		
	        url: url,
	        type: 'GET',
	        data: data,
	        accept : 'application/json',
	        dataType: "json",
	        success: function(content) {
	        	if(callback !== undefined)
	        		callback(content, callback_attr);
	        	$("#loading_page").hide();
	        },error:function(){
	        	$("#loading_page").hide();
	        }
        });
	};
	
	this.countdown = function( element, minutes, seconds , timmerdiv , status )
	{
	    var endTime, hours, mins, msLeft, time;

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
	            if (status == "In Progress"){
	            	$(timmerdiv).removeClass("text_grn");
	            	$(timmerdiv).addClass("text_red");
	            }
	        } else {
	            time = new Date( msLeft );
	            hours = time.getUTCHours();
	            mins = time.getUTCMinutes();
	            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
	            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
	        }
	    }

	    //element = document.getElementById( elementName );
	    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
	    updateTimer();
	}
}