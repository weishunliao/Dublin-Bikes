let time1 = weathers_object_forecast.list[0].dt_txt.substring(11, 16);
let time2 = weathers_object_forecast.list[1].dt_txt.substring(11, 16);
let time3 = weathers_object_forecast.list[2].dt_txt.substring(11, 16);

let temp1 = parseInt(weathers_object_forecast.list[0].main.temp) - 273.15;
let temp2 = parseInt(weathers_object_forecast.list[1].main.temp) - 273.15;
let temp3 = parseInt(weathers_object_forecast.list[2].main.temp) - 273.15;


let weather_id1 = weathers_object_forecast.list[0].weather[0].id;
let weather_id2 = weathers_object_forecast.list[1].weather[0].id;
let weather_id3 = weathers_object_forecast.list[2].weather[0].id;


document.getElementById("time1").innerHTML = time1;
document.getElementById("time2").innerHTML = time2;
document.getElementById("time3").innerHTML = time3;


document.getElementById("temp1").innerHTML = Math.round(temp1) + '&deg  ';
document.getElementById("temp2").innerHTML = Math.round(temp2) + '&deg  ';
document.getElementById("temp3").innerHTML = Math.round(temp3) + '&deg  ';

let num1 = parseInt(weathers_object_forecast.list[0].dt_txt.substring(11, 13));
let num2 = parseInt(weathers_object_forecast.list[1].dt_txt.substring(11, 13));
let num3 = parseInt(weathers_object_forecast.list[2].dt_txt.substring(11, 13));

let nums = [num1, num2, num3];
let ids = [weather_id1, weather_id2, weather_id3];


for (var i = 0; i < 3; i++) {
    if (nums[i] >= 6 && nums[i] <= 18) {
        document.getElementById("icon" + (i + 1)).className = "wi wi-owm-day-" + ids[i];
    } else {
        document.getElementById("icon" + (i + 1)).className = "wi wi-owm-night-" + ids[i];
    }
}

let temp_current = weathers_object_current["main"]["temp"];
let description = weathers_object_current["weather"][0]["main"];
let id = weathers_object_current["weather"][0]["id"];
document.getElementById("temp_current").innerHTML = Math.round(temp_current) + '&deg  ' + description;
let hour = new Date().getHours();
if (hour >= 6 && hour <= 18) {
    document.getElementById('icon0').className = "wi wi-owm-day-" + id;
} else {
    document.getElementById('icon0').className = "wi wi-owm-night-" + id;
}