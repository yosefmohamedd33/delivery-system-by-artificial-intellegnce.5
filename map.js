var map;

// Markers are Points
var markers = [];

// Paths are Polylines
var paths = [];
var distances = [];
var adjacency_matrix = [];

var itb_location = [-6.891117, 107.609875];
var map_style = [
  {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#242f3e"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#746855"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#242f3e"
      }
    ]
  },
  {
    "featureType": "administrative",
    "elementType": "geometry",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.locality",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#d59563"
      }
    ]
  },
  {
    "featureType": "poi",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#d59563"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#263c3f"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#6b9a76"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#38414e"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#212a37"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9ca5b3"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#746855"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#1f2835"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#f3d19c"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "transit",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "transit",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#2f3948"
      }
    ]
  },
  {
    "featureType": "transit.station",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#d59563"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#17263c"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#515c6d"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#17263c"
      }
    ]
  }
]

var addPathButton = document.getElementById('addPathButton');
var getPathButton = document.getElementById('getPathButton');
var selectPath_1 = document.getElementById('path-1');
var selectPath_2 = document.getElementById('path-2');
var selectSource = document.getElementById('source-select');
var selectDestination = document.getElementById('destination-select');
var pointList = document.getElementById('pointList');
var pathList = document.getElementById('pathList');

function initMap() {
  var itb = { lat: itb_location[0], lng: itb_location[1] };

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 16,
    center: itb,
    mapTypeId: 'roadmap',
    styles: map_style
  });

  map.addListener('click', function (e) {
    addMarker(e.latLng, map);
  });
}

function addMarker(latLng, map) {
  updateLabel();
  var marker = new google.maps.Marker({
    position: latLng,
    map: map,
    label: marker_label.toString()
  });

  marker.addListener('dblclick', function () {
    marker.setMap(null);
    markers = markers.filter(item => item !== marker)
    label_stack.push(marker.getLabel());
    label_stack.sort((a, b) => (b - a));

    console.log(markers);
    updatePoints();
    generateDistanceMatrix();
    resetAdjacencyMatrix();
    updateAdjacencyMatrix();
  })

  markers.push(marker);
  console.log(markers);
  updatePoints();
  generateDistanceMatrix();
  resetAdjacencyMatrix();
  updateAdjacencyMatrix();

}

function clearMarker() {
  for (var i = markers.length - 1; i >= 0; i--) {
    markers[i].setMap(null);
    markers.pop(markers[i]);
    marker_label = 1;
    max_label = 1;
  }

  while (label_stack.length != 0) {
    label_stack.pop();
  }

  updatePoints();
  generateDistanceMatrix();
  updateAdjacencyMatrix();
}

// Label 
var marker_label = 1;
var max_label = 1;
var label_stack = [];
var global_shortest_path = [];

function updateLabel() {
  if (label_stack.length != 0) {
    marker_label = label_stack.pop();
  }
  else {
    if (marker_label >= max_label) {
      max_label = marker_label;
    }
    marker_label = max_label++;
  }
}

function findMarkerByLabel(label) {
  for (var i = markers.length - 1; i >= 0; i--) {
    if (markers[i].getLabel() == label) {
      return markers[i];
    }
  }
}

function updatePathSelection() {
  // Update select point
  for (var i = 0; i < markers.length; i++) {
    var option1 = document.createElement('option');
    option1.value = markers[i].getLabel();
    option1.text = markers[i].getLabel().toString();

    var option2 = document.createElement('option');
    option2.value = markers[i].getLabel();
    option2.text = markers[i].getLabel().toString();

    var option3 = document.createElement('option');
    option3.value = markers[i].getLabel();
    option3.text = markers[i].getLabel().toString();

    var option4 = document.createElement('option');
    option4.value = markers[i].getLabel();
    option4.text = markers[i].getLabel().toString();


    selectPath_1.add(option1);
    selectPath_2.add(option2);
    selectSource.add(option3);
    selectDestination.add(option4);
  }
}

function updatePoints() {
  // clear select point
  selectPath_1.options.length = 0;
  selectPath_2.options.length = 0;
  selectSource.options.length = 0;
  selectDestination.options.length = 0;

  // Clear pointlist
  while (pointList.firstChild) {
    pointList.removeChild(pointList.firstChild);
  }

  // Update point list
  for (var i = 0; i < markers.length; i++) {
    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(markers[i].getPosition().toString()));
    pointList.appendChild(entry);
  }

  updatePathSelection();
}

function addPath(marker1, marker2) {
  poly = new google.maps.Polyline({
    strokeColor: '#6e6ed8',
    strokeOpacity: 1,
    strokeWeight: 2,
    map: map,

  });

  try {
    var path = [marker1.getPosition(), marker2.getPosition()];
    poly.setPath(path);
    paths.push(poly);
  } catch {
    console.log("error");
  }

  updatePaths();
  updateAdjacencyMatrix(marker1, marker2);
  console.log(adjacency_matrix);
}

function clearPath() {
  for (var i = paths.length - 1; i >= 0; i--) {
    paths[i].setMap(null);
    paths.pop(paths[i]);
  }

  updatePaths();
}

function clearShortestPath() {

}

function updatePaths() {
  while (pathList.firstChild) {
    pathList.removeChild(pathList.firstChild);
  }

  for (var i = 0; i < paths.length; i++) {
    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(paths[i].getPath().getAt(0).toString() + "\n to \n" + paths[i].getPath().getAt(1).toString()));
    pathList.appendChild(entry);
  }
}

function clearAll() {
  location.reload();

  // clearMarker();
  // clearPath();
}

function calculateDistance(position1, position2) {
  distance = google.maps.geometry.spherical.computeDistanceBetween(position1, position2);
  return distance;
}


function generateDistanceMatrix() {
  distances = [];

  for (var i = 0; i < markers.length; i++) {
    temp_distance = [];

    for (var j = 0; j < markers.length; j++) {

      if (i == j) {
        temp_distance.push(0);
      } else {
        temp_distance.push(calculateDistance(markers[i].getPosition(), markers[j].getPosition()));
      }

    }

    distances.push(temp_distance);
  }

  printDistances();
}

function printDistances() {
  for (var i = 0; i < distances.length; i++) {
    console.log(distances[i]);
  }

}

function resetAdjacencyMatrix() {
  adjacency_matrix = [];

  for (var i = 0; i < markers.length; i++) {
    temp_adj = [];
    for (var j = 0; j < markers.length; j++) {
      temp_adj.push(0);
    }
    adjacency_matrix.push(temp_adj);
  }

}

function updateAdjacencyMatrix() {

  for (var i = 0; i < paths.length; i++) {
    idx1 = -1;
    idx2 = -1;
    for (var j = 0; j < markers.length; j++) {
      if (markers[j].getPosition() === paths[i].getPath().getAt(0)) {
        idx1 = parseInt(markers[j].getLabel());
        break;
      }
    }

    for (var j = 0; j < markers.length; j++) {
      if (markers[j].getPosition() === paths[i].getPath().getAt(1)) {
        idx2 = parseInt(markers[j].getLabel());
        break;
      }
    }

    if (idx1 != -1 && idx2 != -1 && idx1 != idx2) {
      adjacency_matrix[idx1 - 1][idx2 - 1] = 1;
      adjacency_matrix[idx2 - 1][idx1 - 1] = 1;
    }

  }

}

function getMarkerIdxByLabel(label) {

  for (var i = markers.length - 1; i >= 0; i--) {
    if (markers[i].getLabel() == label) {
      return i;
    }
  }

}


function getShortestPath(source, destination) {

  json_data = {
    "source_point": source,
    "destination_point": destination,
    "adjacency_matrix": adjacency_matrix,
    "distance_matrix": distances,
  }

  $.ajax({
    url: "/get-shortest-path/",
    data: JSON.stringify(json_data),
    type: 'post',
    contentType: 'application/json',

    success: function (result) {
      shortest_path = JSON.parse(result);
      shortest_path = shortest_path.map((x) => x + 1);
      console.log(shortest_path);
      showShortestPath(shortest_path);
    }

  });

}

function showShortestPath(shortest_path) {
  if (global_shortest_path.length >= 1) {
    global_shortest_path.map(
      i => {
        if (global_shortest_path.indexOf(i) == global_shortest_path.length - 1) return;
        var poly = new google.maps.Polyline({
          strokeColor: '#6e6ed8',
          strokeOpacity: 1,
          strokeWeight: 3,
          map: map,
        });

        let next_i = global_shortest_path[(global_shortest_path.indexOf(i)) + 1];

        var path = [markers[i - 1].getPosition(), markers[next_i - 1].getPosition()];
        poly.setPath(path);
      }
    )

    global_shortest_path
  }

  global_shortest_path = shortest_path;

  shortest_path.map(
    i => {
      if (shortest_path.indexOf(i) == shortest_path.length - 1) return;
      var poly = new google.maps.Polyline({
        strokeColor: '#fff',
        strokeOpacity: 1,
        strokeWeight: 3,
        map: map,
      });

      let next_i = shortest_path[(shortest_path.indexOf(i)) + 1];


      var path = [markers[i - 1].getPosition(), markers[next_i - 1].getPosition()];
      poly.setPath(path);
    }
  )


}

addPathButton.onclick = function (event) {
  label1 = selectPath_1.options[selectPath_1.selectedIndex].value;
  label2 = selectPath_2.options[selectPath_2.selectedIndex].value;
  marker1 = findMarkerByLabel(label1);
  marker2 = findMarkerByLabel(label2);

  addPath(marker1, marker2);
}

getPathButton.onclick = function (event) {
  from_label = selectSource.options[selectSource.selectedIndex].value;
  to_label = selectDestination.options[selectDestination.selectedIndex].value;
  source = getMarkerIdxByLabel(from_label);
  destination = getMarkerIdxByLabel(to_label);

  getShortestPath(source, destination);
}
