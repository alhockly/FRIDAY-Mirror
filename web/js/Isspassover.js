var weekday = new Array(7);
	weekday[0] =  "Sunday";
	weekday[1] = "Monday";
	weekday[2] = "Tuesday";
	weekday[3] = "Wednesday";
	weekday[4] = "Thursday";
	weekday[5] = "Friday";
	weekday[6] = "Saturday";
	var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

var makeRequest = function (url, method) {

	// Create the XHR request
	var request = new XMLHttpRequest();

	// Return it as a Promise
	return new Promise(function (resolve, reject) {

		// Setup our listener to process compeleted requests
		request.onreadystatechange = function () {

			// Only run if the request is complete
			if (request.readyState !== 4) return;

			// Process the response
			if (request.status >= 200 && request.status < 300) {
				// If successful
				resolve(request);
			} else {
				// If failed
				reject({
					status: request.status,
					statusText: request.statusText
				});
			}

		};

		// Setup our HTTP request
		request.open(method || 'GET', url, true);


		// Send the request
		request.send();

	});
};



    makeRequest("iss.json")

    .then(function (xml) {
		console.log(xml)
        var passoverdata = JSON.parse(xml.responseText)

        i=0
        added=0
        while(added<6){
            risetime = passoverdata.response[i].risetime

            var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
            d.setUTCSeconds(risetime);
            console.log(d)
            if(d.getHours()>17 || d.getHours()<2){

                var datestring =("00" + d.getDate()).slice (-2)+" "+months[d.getMonth()]+" - "+("00" + d.getHours()).slice (-2)+":"+("00" + d.getMinutes()).slice (-2)+":"+("00" + d.getSeconds()).slice (-2)
                var pass = document.createElement("div")
                pass.innerHTML=datestring
                pass.className="isspass"
                document.getElementById("isspasses").appendChild(pass)
                added++;
            }


            i=i+1;
        }

	})
