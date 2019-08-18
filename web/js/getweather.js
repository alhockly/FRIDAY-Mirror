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
Weathercreds=[]

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
		//console.log(xml)
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
		fetchcurrent()

		return makeRequest("http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+citykey+"?metric=true&details=true&apikey="+Weathercreds[0])

	})
	.then(function (xml) {
		fetch5day()

	})


	.catch(function (error) {
		console.log('Something went wrong', error);
	});
}

function fetchcurrent(){
	makeRequest("http://dataservice.accuweather.com/currentconditions/v1/"+citykey+"?details=true&apikey="+Weathercreds[0])

    .then(function (xml) {
    	var currentconditions = JSON.parse(xml.responseText)
		currenttemp = currentconditions[0].RealFeelTemperature.Metric.Value
		weathertext = currentconditions[0].WeatherText
		rainchance = currentconditions[0].HasPrecipitation
		UVindex = currentconditions[0].UVIndex



		console.log(currenttemp)
		console.log(weathertext)
		console.log("rain?",rainchance)
		console.log("UV index",UVindex)


		$("#weathertoday").text(currenttemp+"°C")
		$("#descriptiontoday").text(weathertext)
	})

	.catch(function (error) {
		console.log("error")
	});

}

function fetch5day(){
	makeRequest("http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+citykey+"?metric=true&details=true&apikey="+Weathercreds[0])
	.then(function (xml) {
		console.log(xml)
        ////displaying weather
		var weather=JSON.parse(xml.responseText)

		var fivedayforcast=weather.DailyForecasts
		var days = new Array(5);

		$("#weatherweek").empty()

		i=0
		while(i<5){
			day=fivedayforcast[i]
			rainchance=day.Day.RainProbability
			weather={}
			weather.rainchance=rainchance
			weather.mintemp=day.RealFeelTemperature.Minimum.Value
			weather.maxtemp=day.RealFeelTemperature.Maximum.Value
			weather.desc=day.Day.ShortPhrase
			weather.moonphase=day.Moon.Phase
			days[i]=weather

			var weatherday = document.createElement("div")
			weatherday.id="weatherday"+i
			weatherday.className="weatherday"
			weatherday.innerHTML = weather.mintemp.toFixed()+" - "+weather.maxtemp.toFixed()+"°C  "+weather.desc+" "+weather.rainchance+"%"
			document.getElementById("weatherweek").appendChild(weatherday)
			i++;
		}
		console.log(days)

		$("#todaysrainchance").text(days[0].rainchance+"%")



	})

	.catch(function (error) {
		console.log("error",error)
	});

}


fetchweather()

var getcurrentinterval= setInterval(fetchcurrent,2400000)	//every 30 mins as accuweather only allow 50 requests a day
var getforcastinterval= setInterval(fetch5day,43200000 )	//every 12 hours