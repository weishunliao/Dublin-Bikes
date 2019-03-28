var markers = [];
var map;
var active_marker_obj;
var directionsService;
var directionsDisplay;

function myMap() {

    var styledMapType = new google.maps.StyledMapType(
        [
            {
                "featureType": "administrative",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#d6e2e6"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#cfd4d5"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#7492a8"
                    }
                ]
            },
            {
                "featureType": "administrative.neighborhood",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "lightness": 25
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#dde2e3"
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#cfd4d5"
                    }
                ]
            },
            {
                "featureType": "landscape.natural",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#dde2e3"
                    }
                ]
            },
            {
                "featureType": "landscape.natural",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#7492a8"
                    }
                ]
            },
            {
                "featureType": "landscape.natural.terrain",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#dde2e3"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#588ca4"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "saturation": -100
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#a9de83"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#bae6a1"
                    }
                ]
            },
            {
                "featureType": "poi.sports_complex",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#c6e8b3"
                    }
                ]
            },
            {
                "featureType": "poi.sports_complex",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#bae6a1"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#41626b"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "saturation": -45
                    },
                    {
                        "lightness": 10
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#c1d1d6"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#a6b5bb"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#9fb6bd"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "transit",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "saturation": -70
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#b4cbd4"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#588ca4"
                    }
                ]
            },
            {
                "featureType": "transit.station",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "transit.station",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#008cb5"
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "transit.station.airport",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": -5
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#a6cbe3"
                    }
                ]
            }
        ]
        , {name: 'Styled Map'}
    );
    var mapProp = {
        center: new google.maps.LatLng(53.3471, -6.26059),
        zoom: 13,
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false
    };
    var my_location;
    navigator.geolocation.getCurrentPosition(function (position) {
        let geo = {};
        geo.lat = position.coords.latitude;
        geo.lng = position.coords.longitude;
        // geo.lat=53.3375;
        // geo.lng = -6.25294;
        let img = {
            url: 'static/img/pin.svg',
            origin: new google.maps.Point(0, 0),
            scaledSize: new google.maps.Size(50, 50)
        };
        my_location = new google.maps.Marker({
            position: geo,
            map: map,
            title: "geolocation",
            icon: img,
        });
    });
    map = new google.maps.Map(document.getElementById('bike_map'), mapProp);
    map.mapTypes.set('styled_map', styledMapType);
    map.setMapTypeId('styled_map');
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);

    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(53.281561, -6.364376),
        new google.maps.LatLng(53.400044, -6.215727));

    var input1 = document.getElementById('route_start');
    var input2 = document.getElementById('route_end');
    var options = {
        bounds: defaultBounds,
        types: ['establishment']
    };
    var autocomplete1 = new google.maps.places.Autocomplete(input1, options);
    var autocomplete2 = new google.maps.places.Autocomplete(input2, options);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response_json = JSON.parse(this.responseText);
            draw_marker(response_json)
        }
    };
    xhttp.open("GET", "/update_map?t=current", true);
    xhttp.send();
}

function draw_marker(response_json) {
    markers = [];
    for (let i = 0; i < response_json.length; i++) {
        let image = {};
        image.origin = new google.maps.Point(0, 0);
        image.scaledSize = new google.maps.Size(30, 30);
        if (response_json[i].available_bikes > 10 && response_json[i].status == "OPEN") {
            image.url = 'static/img/green.png';
        } else if (response_json[i].available_bikes > 0 && response_json[i].status == "OPEN") {
            image.url = 'static/img/orange.png';
        } else if (response_json[i].available_bikes == 0 && response_json[i].status == "OPEN") {
            image.url = 'static/img/red.png';
        } else {
            image.url = 'static/img/grey.png';
        }

        // let content = "<div>";
        var marker = new google.maps.Marker({
            position: {lat: response_json[i].position.lat, lng: response_json[i].position.lng},
            map: map,
            icon: image,
            title: String(response_json[i].name)
        });
        // content += "<h4>Station: " + response_json[i].name + "</h4>";
        // content += "<p>Available bike stands: " + response_json[i].available_bike_stands + "<br>";
        // content += "Available bikes: " + response_json[i].available_bikes + "<br></p>";
        // content += "</div>";
        let banking;
        if (response_json[i].banking == true) {
            banking = "Yes";
        } else {
            banking = "No";
        }
        let content = '<div class="container" style="font-family: Rubik;padding: 0;">\n' +
            '    <div class="row" style="">\n' +
            '        <div class="col-12" style="padding: 0">\n' +
            '            <div id="wrap-box_now">\n' +
            '                <div class="row justify-content-center" style=";margin: 20px">\n' +
            '                    <div class=\'col-12 justify-content-center\' style=";text-align: center;">\n' +
            '                        <h2 style="font-size: 1.5rem;">' + response_json[i].number + ' - ' + response_json[i].name + '</h2>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div class="row justify-content-center" style=";margin: 20px;">\n' +
            '                    <div class="col-2 d-flex" style="background-color: #efefef;align-items: center">\n' +
            '                        <img src="static/img/bicycle.svg" width="100%" height="100%">\n' +
            '                    </div>\n' +
            '                    <div class="col-10 d-flex"\n' +
            '                         style=";background-color: lightgrey;align-items: center;color: black">\n' +
            '                        <div style="text-align: center;font-size: 13pt;">\n' +
            '                            <span>Available bikes: ' + response_json[i].available_bikes + '</span>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div class="row justify-content-center" style=";margin: 20px;">\n' +
            '                    <div class="col-2 d-flex" style="background-color: #efefef;align-items: center">\n' +
            '                        <img src="static/img/parking.svg" width="100%" height="100%">\n' +
            '                    </div>\n' +
            '                    <div class="col-10 d-flex"\n' +
            '                         style=";background-color: lightgrey;align-items: center;">\n' +
            '                        <div class="" style="margin: 0;font-size: 13pt;">\n' +
            '                            <span>Free stands: ' + response_json[i].available_bike_stands + '</span>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div class="row justify-content-center" style=";;;margin: 20px">\n' +
            '                    <div class="col-2 d-flex" style="background-color: #efefef;align-items: center">\n' +
            '                        <img src="static/img/visa.svg" width="100%" height="100%">\n' +
            '                    </div>\n' +
            '                    <div class="col-10 d-flex"\n' +
            '                         style=";background-color: lightgrey;align-items: center;">\n' +
            '                        <div style="text-align: center;font-size: 13pt;">\n' +
            '                            <span>Credit cards: ' + banking + '</span>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '            <div id="wrap-box_feature" style="display: none;">\n' +
            '                <div class="row justify-content-center" style=";margin: 20px">\n' +
            '                    <div class=\'col-12 justify-content-center\' style=";text-align: center;">\n' +
            '                        <h2 style="font-size: 1.5rem;">Next 2 Hours</h2>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div class="row justify-content-center" style=";margin: 20px">\n' +
            '                    <div class="col-2 d-flex" style="background-color: #efefef;align-items: center">\n' +
            '                        <img src="static/img/bicycle.svg" width="100%" height="100%">\n' +
            '                    </div>\n' +
            '                    <div class="col-10 d-flex"\n' +
            '                         style=";background-color: lightgrey;align-items: center;color: black">\n' +
            '                        <div style="text-align: center;font-size: 13pt;;">\n' +
            '                            <span>Available bikes: 5</span>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div class="row justify-content-center" style=";margin: 20px">\n' +
            '                    <div class="col-2 d-flex" style="background-color: #efefef;align-items: center">\n' +
            '                        <img src="static/img/parking.svg" width="100%" height="100%">\n' +
            '                    </div>\n' +
            '                    <div class="col-10 d-flex"\n' +
            '                         style=";background-color: lightgrey;align-items: center;">\n' +
            '                        <div class="" style="margin: 0;font-size: 13pt;;">\n' +
            '                            <span>Free stands: 27</span>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div class="row justify-content-center" style=";;;margin: 20px">\n' +
            '                    <div class="col-2 d-flex" style="background-color: #efefef;align-items: center">\n' +
            '                        <img src="static/img/visa.svg" width="100%" height="100%">\n' +
            '                    </div>\n' +
            '                    <div class="col-10 d-flex"\n' +
            '                         style=";background-color: lightgrey;align-items: center;">\n' +
            '                        <div style="text-align: center;font-size: 13pt;">\n' +
            '                            <span>Credit cards accept: NO</span>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '            <div id="wrap-box_past24" style="display:none">\n' +
            '                <div class="row justify-content-center" style=";padding: 0;">\n' +
            '                    <div id="chart_div" style="padding: 0">\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '            <div class="row justify-content-center" style=";margin: 20px">\n' +
            '                <div class="col-4 d-flex justify-content-center" style=";align-items: center;">\n' +
            '                    <button type="button" class="btn btn-outline-info button_font_size" style=";padding: 1px 6px;" onclick="to_past24()">\n' +
            '                        Past 24\n' +
            '                    </button>\n' +
            '                </div>\n' +
            '                <div class="col-4 d-flex justify-content-center" style=";align-items: center;">\n' +
            '                    <button type="button" class="btn btn-outline-info button_font_size" style="padding: 1px 15px" onclick="to_now()">\n' +
            '                        Now\n' +
            '                    </button>\n' +
            '                </div>\n' +
            '                <div class="col-4 d-flex justify-content-center" style="align-items: center;">\n' +
            '                    <button type="button" class="btn btn-outline-info button_font_size" style="padding: 1px 15px;" onclick="to_feature()">\n' +
            '                        Feature\n' +
            '                    </button>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '        </div>\n' +
            '\n' +
            '    </div>\n' +
            '</div>';
        let mker = {};
        mker.title = marker.title;
        mker.obj = marker;
        mker.content = content;
        mker.lat = response_json[i].position.lat;
        mker.lng = response_json[i].position.lng;
        mker.available_bike = response_json[i].available_bikes;
        mker.available_bike_stands = response_json[i].available_bike_stands;
        markers.push(mker);
        show_info(marker, content);
    }
}

function clear_markers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].obj.setMap(null);
    }
}

function show_info(marker, content) {
    var infowindow = new google.maps.InfoWindow({
        content: content,
        maxWidth: 500
    });
    marker.addListener("click", function () {
        if (active_marker_obj != null) {
            active_marker_obj.close();
        }
        active_marker_obj = infowindow;
        infowindow.open(marker.get("map"), marker);
    });
}

google.charts.load('current', {'packages': ['corechart']});


function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Year', 'Sales', 'Expenses'],
        ['2013', 1000, 400],
        ['2014', 1170, 460],
        ['2015', 660, 1120],
        ['2016', 1030, 540]
    ]);

    var options = {
        title: 'Company Performance',
        legend: {position: 'none'},
        chartArea: {'width': '75%', 'height': '80%'},
    };

    var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}


function getDistance(x_1, x_2, y_1, y_2) {
    let n = (x_1 - x_2) * (x_1 - x_2) + (y_1 - y_2) * (y_1 - y_2);
    return Math.sqrt(n);
}


function calcRoute() {
    let start = document.getElementById('route_start').value;
    let url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + start + "&key=AIzaSyC8LCHyymh52e52Y0-UM6NEfRbERgst13A";
    var start_station_index = 0;
    let wpts = [];
    $.get(url, function (data, status) {
        let lat = (data.results)[0].geometry.location.lat;
        let lng = (data.results)[0].geometry.location.lng;
        let min = getDistance(lat, markers[0].lat, lng, markers[0].lng);
        for (let i = 1; i < markers.length; i++) {
            let dis = getDistance(lat, markers[i].lat, lng, markers[i].lng);
            if (dis < min && markers[i].available_bike >= 5) {
                min = dis;
                start_station_index = i;
            }
        }
        let start_point = {
            location: {lat: markers[start_station_index].lat, lng: markers[start_station_index].lng},
            stopover: true
        };
        wpts.push(start_point);
    });
    let end = document.getElementById('route_end').value;
    var end_station_index = 0;
    $.get(url, function (data, status) {
        let lat = (data.results)[0].geometry.location.lat;
        let lng = (data.results)[0].geometry.location.lng;
        let min = getDistance(lat, markers[0].lat, lng, markers[0].lng);
        for (let i = 1; i < markers.length; i++) {
            let dis = getDistance(lat, markers[i].lat, lng, markers[i].lng);
            if (dis < min && markers[i].available_bike_stands >= 5) {
                min = dis;
                end_station_index = i;
            }
        }
        let end_point = {
            location: {lat: markers[end_station_index].lat, lng: markers[end_station_index].lng},
            stopover: true
        };
        wpts.push(end_point);
    });
    var request = {
        origin: start,
        destination: end,
        travelMode: 'BICYCLING',
        waypoints: wpts
    };
    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            clear_markers();
            directionsDisplay.setDirections(result);
        }
    });
}