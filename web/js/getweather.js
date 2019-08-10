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

citykey=""

///sick promise chain

function fetchweather(){
	makeRequest('AccuweatherKeys.json')
	.then(function (xml) {
		//console.log(xml.responseText);
		Weathercreds=[]
        Weathercreds.push(xml.responseText);
		console.log(Weathercreds[0])
        return makeRequest("location.json")

	})
    .then(function (xml) {
		console.log(xml)
        var locationobj = JSON.parse(xml.responseText)
        var city = locationobj["city"]
        return makeRequest("http://dataservice.accuweather.com/locations/v1/cities/search?q="+city+"&apikey="+Weathercreds[0])
	})
    .then(function (xml) {
		//console.log(xml)
        citykey= JSON.parse(xml.responseText)[0].Key
		console.log(citykey)
        return makeRequest("http://dataservice.accuweather.com/currentconditions/v1/"+citykey+"?details=true&apikey="+Weathercreds[0])
	})
    .then(function (xml) {
		//console.log(xml)

		var currentconditions = JSON.parse(xml.responseText)
		currenttemp = currentconditions[0].RealFeelTemperature.Metric.Value
		weathertext = currentconditions[0].WeatherText
		console.log(currenttemp)
		console.log(weathertext)

		$("#weathertoday").text(currenttemp)
		$("#descriptiontoday").text(weathertext)

		return makeRequest("http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+citykey+"?metric=true&details=true&apikey="+Weathercreds[0])

	})
	.then(function (xml) {
		//console.log(xml)
        ////displaying weather
		var weather=JSON.parse(xml.responseText)
		var currentheadline=weather.Headline.Text
		var currentcategory=weather.Headline.Category
		var fivedayforcast=weather.DailyForecasts



	})


	.catch(function (error) {
		console.log('Something went wrong', error);
	});
}

fetchweather()
var getweatherinterval= setInterval(fetchweather,1800000)	//every 30 mins as accuweather only allow 50 requests a day