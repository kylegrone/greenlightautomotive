function messagePuller(){
	/*
	 * this function is used as an observer to all changes on the server
	 * it conencts to a channel in which  most cases will be the dealer id
	 * if it receives any message it will inform the attached widgets
	 * 
	 */
	self= this
	this.centrifuge_url =null;
	this.secret = null;
	this.user = null;
	this.user_nick = null;
	this.token = null;
	this.centrifuge = null
	this.user = ""
	this.widgets = [] //format {"name":"","callback":"","services_listening_to":[]}
	
	
	self.addWidgets = function(widget){
		/*
		 * Add listeners
		 * 
		 */
		this.widgets.push(widget);
	}
	
	
	this.setCentrifuge = function(){
		console.info(self)
		console.info("setting centrifuge")
		this.setTimeStamp();
		this.settoken()
		 self.centrifuge = new Centrifuge({
		    // please, read Centrifuge documentation to understand 
		    // what does each option mean here
		    "url": this.centrifuge_url,
		    "user": self.user,
		    "timestamp": self.timestamp,
		    "token": self.token,
		    "debug": true
		});
		
		self.centrifuge.on('connect', function() {
		    console.info("connected to Centrifugo");
		    self.subscribe();
		    setInterval(function() {
		        // Heroku closes inactive websocket connection after 55 sec,
		        // so let's send ping message periodically
		        self.centrifuge.ping();
		    }, 40000);
		});
		
		self.centrifuge.on('disconnect', function(){
		    console.info('disconnected from Centrifuge');
		});
		
	}
	this.subscribe = function(){
		 var subscription = this.centrifuge.subscribe(this.channel, function(message) {
			 	console.info(message)
		        if (message.data) {
		        	console.info(message.data);
		        	if(typeof message.data["services"]!= "undefined"){
		        		
		        		$(self.widgets).each(function(k,v){
	        				if(self.checkServiceAllowed(self.widgets[k]["services_listening_to"], message.data["services"])){
	        					
	        					self.widgets[k].callback(message.data)
	        				}
		        		});
		        	}
		         }
		    });
		
		    subscription.on('ready', function() {
		        console.info("subscribed on channel custom-chat");
		        subscription.presence(function(message) {
		            var count = 0;
		            for (var key in message.data){
		                count++;
		            }
		           
		        });
		        
		    });
		    
		    subscription.on('join', function(message) {
		        console.info('someone joined channel');
		    });
		
		    subscription.on('leave', function(message) {
//		        console.info('someone left channel');
		    });
		    subscription.history(function(message) {
			    console.info("history");
				
	 			
	        });
	}
	this.checkServiceAllowed= function(widget_service,service_changed){
		for(var i = 0; i<widget_service.length; i++){
		    for(var j=0; j<service_changed.length; j++){
		        if(widget_service[i] === service_changed[j]){
		            return true;
		        }
		    }
		}
		return false;
	}
	this.connect = function(){
		self.centrifuge.connect();
	}
	this.settoken = function(){
		var hmacBody = self.user + self.timestamp;
		var shaObj = new jsSHA("SHA-256", "TEXT");
		shaObj.setHMACKey(self.secret, "TEXT");
		shaObj.update(hmacBody);
		this.token = shaObj.getHMAC("HEX");
		console.info(this.token)
	}
	
	this.getCurrentTime = function(){
		 var pad = function (n) {return ("0" + n).slice(-2);};
		    var d = new Date();
		    return pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
	}
	
	this.getTimeFromTimestamp = function(timestamp){
		 var pad = function (n) {return ("0" + n).slice(-2);};
		 var d = new Date(timestamp *1000);
		 return pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
	}
	this.setTimeStamp = function(){
		 this.timestamp = parseInt(new Date().getTime()/1000).toString();
	}
	this.getCurrentTimeStamp = function(){
		return parseInt(new Date().getTime()/1000).toString();
	}
}