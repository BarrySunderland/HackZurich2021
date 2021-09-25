import React, { useState } from "react";
import {
  GoogleMap,
  Circle,
  useJsApiLoader,
  DirectionsRenderer,
} from "@react-google-maps/api";
import { getColorByCondition } from "../utils/utils";
const google = window.google;

const containerStyle = {
  width: "100%",
  height: "800px",
};

/*
const START_CITY = {
  lat: 47.30471,
  lng: 8.05152,
};

const DEST_CITY = {
  lat: 47.24345,
  lng: 8.18706,
};
const sensorsMap = [
    {
      id: 1,
      name: "Sensor 1",
      Latitude: "47.298730",
      Longitude: "8.120420",
      condition: 0,
    },
  {
    id: 2,
    name: "Sensor 2",
    Latitude: "47.280394",
    Longitude: "8.153229",
    condition: 1,
  },
  {
    id: 3,
    name: "Sensor 3",
    Latitude: "47.269911",
    Longitude: "8.172112",
    condition: 2,
  },
];
*/
function Map({ actualFailures, predictedFailures, zoom, center, onChartOpen }) {
  const [map, setMap] = React.useState(null);
  const [directions, setDirections] = useState(null);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    const directionsService = new google.maps.DirectionsService();
    directionsService.route(
      {
        origin: "schöftland",
        destination: "Menziken",
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        console.log(result);
        if (status === google.maps.DirectionsStatus.OK) {
          setDirections(result);
        } else {
          setError(result);
        }
      }
    );
  });
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: "AIzaSyAUy0PV7tbaUPr-mgjvu13culLRfHSrfSc",
  });

  const onLoad = React.useCallback(function callback(map) {
    const bounds = new window.google.maps.LatLngBounds();
    map.fitBounds(bounds);
    setMap(map);
  }, []);

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null);
  }, []);
  {
    console.log("IIIIII", predictedFailures);
  }
  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      zoom={zoom}
      center={center}
      onLoad={onLoad}
      onUnmount={onUnmount}
    >
      <DirectionsRenderer
        directions={directions}
        options={{
          suppressMarkers: true,
          polylineOptions: { strokeColor: "blue" },
        }}
      />
      {predictedFailures.map((place) => (
        <Circle
          radius={300}
          center={{
            lat: parseFloat(place.Latitude),
            lng: parseFloat(place.Longitude),
          }}
          options={{
            fillColor: getColorByCondition(place.condition),
            strokeColor: getColorByCondition(place.condition),
          }}
          //options={place.circle.options}
        />
      ))}

      {actualFailures.map((place) => (
        <Circle
          radius={300}
          center={{
            lat: parseFloat(place.Latitude),
            lng: parseFloat(place.Longitude),
          }}
          options={{
            fillColor: getColorByCondition(place.condition),
            strokeColor: getColorByCondition(place.condition),
          }}
          //options={place.circle.options}
        />
      ))}
    </GoogleMap>
  ) : (
    <></>
  );
}
export default React.memo(Map);
