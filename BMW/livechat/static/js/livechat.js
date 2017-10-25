function liveChat(){
	var self = this
	this.centrifuge_url =null;
	this.secret = null;
	this.user = null;
	this.user_nick = null;
	this.chat_box = null;
	this.chat_message_box = null;
	this.channel = null;
	this.token = null;
	this.centrifuge = null
	this.timestamp = null
	this.send_button = null
	this.msg_loading_cls = "message_pending"
	this.loading_el = null
	this.extra_detials_el = null
	this.upload_form = $('#upload_form')
	this.setCentrifuge = function(){
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
	this.connect = function(){
		self.centrifuge.connect();
	}
	this.settoken = function(){
		var hmacBody = this.user + this.timestamp;
		var shaObj = new jsSHA("SHA-256", "TEXT");
		shaObj.setHMACKey(self.secret, "TEXT");
		shaObj.update(hmacBody);
		this.token = shaObj.getHMAC("HEX");
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
	
	
	
	
	this.subscribe = function(){
		 var subscription = this.centrifuge.subscribe(this.channel, function(message) {
		        if (message.data) {
		        	if(message.data["user"]!=self.user){
		        		if(message.data["type"]=="typing"){
		        			var msg = message["data"]["nick"]+" "+message["data"]["input"];
		        			self.extra_detials_el.show()
		        			self.extra_detials_el.html(msg);//.delay(4000).hide()
		        			 setTimeout(function() {
		        				 self.extra_detials_el.hide()
		        			    }, 5000);
		        		}else{
		        			self.add_message(message,true)
		        		}
		        	}else{
		        	 var msg_id = message.data["user"] +message.data["msg_id"];
		        	 $("#"+msg_id).removeClass(self.msg_loading_cls)
		        		
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
		            console.info('now connected ' + count + ' clients');
		            self.send_button.removeAttr("disabled");
		            self.chat_message_box.removeAttr("disabled");
		            self.loading_el.hide()
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
				self.history(message)
	 			
	        });
	}
	
	
	this.history =function(history){
		console.info(history.data)
		if(typeof history.data !="undefined" && history.data.length > 0){
			$.each(history.data,function(k,v){
				if(v.data["type"]!="typing" && v.data["type"]!="erasing"){
					self.add_message(v)
				}
			})
		}
	}
	
	this.setTimeStamp = function(){
		 this.timestamp = parseInt(new Date().getTime()/1000).toString();
	}
	this.getCurrentTimeStamp = function(){
		return parseInt(new Date().getTime()/1000).toString();
	}
	
	this.add_message = function(data,append,loader) {
		console.info("ading message");
		if(typeof append != "undefined" && append == true){
			self.chat_box.append(self.create_message(data,loader))
		}else{
			self.chat_box.prepend(self.create_message(data,loader))
		}
		var innerHeight = self.chat_box.prop("scrollHeight")
		self.chat_box.animate({
	          scrollTop: innerHeight 
	     },1000);
		
	}
	this.create_message = function(data,loader) {
		console.info("creating message");
		console.info(data)
		var message = $('<div class="chat_message bubble"></div>');
		var msg_cls=  "";
		if(typeof data["data"]["input"] != "undefined"){
			var msg_id = data["data"]["user"] +data["data"]["msg_id"];
			message.prop("id",msg_id);
			if(typeof loader !="undefined"){
				message.addClass(self.msg_loading_cls);//adding the pending class so it could be removed later
			}
			if (data["data"]["user"] != self.user){
					var msg_cls="other_user bubble--alt";
			}
			message.addClass(msg_cls)
			var time = self.getCurrentTime();
			if(typeof data["data"]["type"] !="undefined" &&  data["data"]["type"] =="image"){
				var input_span = $('<a target="_blank"> </a>');
				var img = $("<img height='100px' width='100px'/>")
				img.attr("src",data["data"]['input'])
				input_span.attr("href",data["data"]["input"]);
				input_span.append(img);
			}else{
				var input_span = $('<span class="text"></span>');
				input_span.text(data["data"]["input"])
			}
			var time_span = $('<span class="time"></span>');
		    var from_span = $('<span class="from"></span>');
		    //time_span.text(self.getTimeFromTimestamp(data["timestamp"]));
		    //from_span.text(data["data"]["nick"]+":");
		    message.append(time_span).append(from_span).append(input_span);
		    return message;
		}
	}

	
	this.sendChat=function(e){
		// input.on('keypress', function(e) {
		var input = self.chat_message_box
		var nickname  = self.user_nick   
//	        var nick = nickname.val();
        if (nickname.length === 0) {nickname = "anonymous";}
        data = {
            "nick": nickname,
            "input": input.val(),
            "user":self.user,
            "msg_id":self.getCurrentTimeStamp()
            
        }
        var message = {"data":data,"timestamp":self.getCurrentTimeStamp()}
        self.centrifuge.publish(this.channel, data);
        self.add_message(message,true,true)
        input.val('');
	    

	}
	
	this.sendImage=function(img){
		if (typeof img != "undefined"){
			var nickname  = self.user_nick
	//	        var nick = nickname.val();
		        if (nickname.length === 0) {nickname = "anonymous";}
			        data = {
			            "nick": nickname,
			            "input": img,
			            "user":self.user,
			            "type":"image",
			            "msg_id":self.getCurrentTimeStamp()
			            
			        }
			    var message = {"data":data,"timestamp":self.getCurrentTimeStamp()}
		        self.centrifuge.publish(self.channel, data);
		        self.add_message(message,true,true)
		}
	}
	this.sendDelete=function(img){
		
		var nickname  = self.user_nick
//	        var nick = nickname.val();
	        if (nickname.length === 0) {nickname = "anonymous";}
		        data = {
		            "nick": nickname,
		            "input": "is erasing a message",
		            "user":self.user,
		            "type":"erasing",
		            "msg_id":self.getCurrentTimeStamp()
		            
		        }
		    var message = {"data":data,"timestamp":self.getCurrentTimeStamp()}
	        self.centrifuge.publish(self.channel, data);
//	        self.add_message(message,true,true)
	    
	}
	this.sendTyping=function(img){
		
		var nickname  = self.user_nick
//	        var nick = nickname.val();
	        if (nickname.length === 0) {nickname = "anonymous";}
		        data = {
		            "nick": nickname,
		            "input": "is typing a message...",
		            "user":self.user,
		            "type":"typing",
		            "msg_id":self.getCurrentTimeStamp()
		            
		        }
		    var message = {"data":data,"timestamp":self.getCurrentTimeStamp()}
	        self.centrifuge.publish(self.channel, data);
//	        self.add_message(message,true,true)
	    
	}
	
	
	this.setEvents = function(){
		var input = self.chat_message_box
		self.chat_message_box.keypress(function(e){
			 if (e.keyCode === 13 && self.centrifuge.isConnected() === true) {
			        var text = input.val();
			        if (text.length === 0) {
			            return;
			        }
			        self.sendChat(e);
			 }else if ((e.keyCode === 8 || e.keyCode === 46) && self.centrifuge.isConnected() === true){
				 self.sendDelete(e)
			 }else if( self.centrifuge.isConnected() === true){
				 self.sendTyping(e)
			 }
		});
		self.send_button.click(function(e){
			self.sendChat(e);
		});
	}
	self.upload = function (event) {
		
		event.preventDefault();
		var data = new FormData(self.upload_form.get(0));
		console.info(data);
		$.ajax({
		    url: $(this).attr('action'),
		    type: $(this).attr('method'),
		    data: data,
		    cache: false,
		    processData: false,
		    contentType: false,
		    success: function(data) {
		    	self.sendImage(data["imgurl"])
		        //livechat.uploadImage(data["/*  */imgurl"]);
		    	
		    }
	});
		return false;
	}
}



