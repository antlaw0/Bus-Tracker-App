  var socket = io.connect('https://agile-sea-57808.herokuapp.com')
//var socket = io.connect('https://localhost:5000')
console.log('test')
  socket.on('connect', function() {
            socket.emit('hello', {data: 'I\'m connected!'});
    });


    
    

    socket.on("new_message_received", function(new_message){
		//split new_message at ;, returns array with bus name and new status
		var dataArray=new_message.split(";")
		//usefirst element in array to get the proper button
		var button = document.getElementById(dataArray[0])
		button.value=dataArray[1]
    })

function changeStatus(busName){
	console.log(busName)
	var busButton=document.getElementById(busName)
	
	if (busButton.value == "unarrived"){
		busButton.value="arrived"
	}
	else if (busButton.value == "arrived"){
		busButton.value="departed"
	}
	else if (busButton.value == "departed"){
		busButton.value="late"
	}
	else if (busButton.value == "late"){
		busButton.value="unarrived"
	}
	
	
	else {
		busButton.value="unarrived"
	}
	text=busName+";"+busButton.value
	
	//emit name of bus and updated status
	socket.emit("new_message", text);
	
	//make AJAX call to update database with status of bus
	$.ajax( {
    url: "/updateDatabase",
    method: "POST",
    data: { busString : text }
  }).done(function(data){
    // data returned here
    console.log(data);
    
  }).fail(function(err){
    // deal with errors here
	console.log("AJAX to update database failed.")
  })


}//end of changeStatus


