import { GoogleMap, Polyline, Marker } from '@react-google-maps/api';
import { useState } from 'react';

const containerStyle = {
  width: '100%',
  height: '400px'
};
const decodePath = (encoded) => {
  if (!encoded) return [];
  
  const poly = [];
  let index = 0, len = encoded.length;
  let lat = 0, lng = 0;

  while (index < len) {
    let shift = 0, result = 0;
    let byte;
    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);
    const dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lat += dlat;

    shift = 0;
    result = 0;
    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);
    const dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lng += dlng;

    poly.push({ lat: lat * 1e-5, lng: lng * 1e-5 });
  }
  return poly;
};


const Map = ({ route, stops, fuelStops }) => {
  const [map, setMap] = useState(null);

  // Default center (can be updated based on route)
  const center = route?.path?.[0] || { lat: 40.7128, lng: -74.0060 };

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={8}
      onLoad={setMap}
    >
      {route?.polyline && (
        <Polyline
          path={decodePath(route.polyline)}
          options={{
            strokeColor: '#2196F3',
            strokeWeight: 3,
          }}
        />
      )}

      {stops?.map((stop, index) => (
        <Marker
          key={`stop-${index}`}
          position={stop.location}
          label={stop.type}
        />
      ))}

      {fuelStops?.map((stop, index) => (
        <Marker
          key={`fuel-${index}`}
          position={stop.geometry.location}
        />
      ))}
    </GoogleMap>
  );
};

export default Map;