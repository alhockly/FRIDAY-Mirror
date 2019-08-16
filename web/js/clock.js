
var dateobj = new Date()
//invokes functions as soon as window loads
window.onload = function(){
	time();
	//meridian();
	whatDay();
	//getdate();
	//uniWeek();
	setInterval(function(){
		dateobj = new Date()
		time();
		//meridian();
		whatDay();
		//getdate();
	}, 60000);
};

//Show todays date, a single number
function getdate(){

    element = document.getElementById("date");

    element.innerText=dateobj.getDate();
}


//gets current time and changes html to reflect it
function time(){
	var	hours = dateobj.getHours(),
		minutes = dateobj.getMinutes(),
		seconds = dateobj.getSeconds();

	//make clock a 12 hour clock instead of 24 hour clock
	hours = (hours > 12) ? (hours - 12) : hours;
	hours = (hours === 0) ? 12 : hours;

	//invokes function to make sure number has at least two digits
	hours = addZero(hours);
	minutes = addZero(minutes);
	seconds = addZero(seconds);

	//changes the html to match results
	$("#clock").text(hours+":"+minutes)
	//document.getElementsByClassName('hours')[0].innerHTML = hours;
	//document.getElementsByClassName('minutes')[0].innerHTML = minutes;
	//document.getElementsByClassName('seconds')[0].innerHTML = seconds;
}

//turns single digit numbers to two digit numbers by placing a zero in front
function addZero (val){
	return (val <= 9) ? ("0" + val) : val;
}

//lights up either am or pm on clock
function meridian(){
	var hours = dateobj.getHours();
	am = document.getElementsByClassName("am")[0].classList;
	pm = document.getElementsByClassName("pm")[0].classList;
	
	(hours >= 12) ? pm.add("light-on") : am.add("light-on");				 //am
	(hours >= 12) ? am.remove("light-on") : pm.remove("light-on");           //pm
}


//lights up what day of the week it is
function whatDay(){
	
	var weekday = new Array(7);
	weekday[0] =  "Sunday";
	weekday[1] = "Monday";
	weekday[2] = "Tuesday";
	weekday[3] = "Wednesday";
	weekday[4] = "Thursday";
	weekday[5] = "Friday";
	weekday[6] = "Saturday";

	var day = weekday[dateobj.getDay()];
	
	$("#day").text(addZero(dateobj.getDate())+" "+day)


}

