  // 2. Runs when the JavaScript framework is loaded
LINKEDIN_AUTHORIZED = false
  function liAuth(){
	  if (LINKEDIN_AUTHORIZED == false){
		   IN.User.authorize(function(){
			   LINKEDIN_AUTHORIZED = true
			  
		   });
	  }else{
		  onLinkedInAuth();
	  }
}
  function onLinkedInLoad() {
    IN.Event.on(IN, "auth", onLinkedInAuth);
  }

  // 2. Runs when the viewer has authenticated
  function onLinkedInAuth() {
    IN.API.Profile("me").fields("first-name", "last-name", "email-address","location").result(displayProfiles).error(function (data) {
        console.log(data);
    });
  }

  // 2. Runs when the Profile() API call returns successfully
  function displayProfiles(profiles) {
    member = profiles.values[0];
    console.info(member);
    $("#first_name_id").val(member.firstName);
    $("#last_name_id").val(member.lastName);
    if( typeof member.emailAddress !="undefined"){
  	  $("#id_email_1").val(member.emailAddress)
    }
    if( typeof member.location !="undefined"){
    	if(typeof member.location.country !="undefined"){
    		var country  = member.location.country.code;
    		$('#id_country').val(country.toUpperCase());
    	}
  	  $("#address_id").val(member.location.name);
  	 
    }
    /*
    document.getElementById("profiles").innerHTML = 
      "<p id=\"" + member.id + "\">Hello " +  member.firstName + " " + member.lastName + "</p>";*/
  }