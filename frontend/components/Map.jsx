// components/Map.jsx
import { 
  GoogleMap, 
  Polyline,
  InfoWindow,
  Marker // Keep regular Marker as fallback
} from '@react-google-maps/api';
import { useState } from 'react';

const containerStyle = {
  width: '100%',
  height: '400px'
};

// Define libraries at component level
const libraries = ['places', 'marker'];

const markerColors = {
  pickup: '#2196F3',
  dropoff: '#F44336',
  break: '#FFC107',
  fuel: '#4CAF50',
  default: '#757575'
};

const Map = ({ route, stops, fuelStops }) => {
  const [selectedMarker, setSelectedMarker] = useState(null);
  const [map, setMap] = useState(null);

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

  const path = route?.polyline ? decodePath(route.polyline) : [];
  const center = path[0] || { lat: 40.7128, lng: -74.0060 };

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={8}
      onLoad={setMap}
    >
      {path.length > 0 && (
        <Polyline
          path={path}
          options={{
            strokeColor: '#2196F3',
            strokeWeight: 3,
          }}
        />
      )}

      {/* Use regular Markers with custom labels */}
      {stops?.map((stop, index) => (
        <Marker
          key={`stop-${index}`}
          position={stop.location}
          label={{
            text: stop.type === 'break' ? '⏸️' : 
                  stop.type === 'pickup' ? '🔵' :
                  stop.type === 'dropoff' ? '🔴' : '📍',
            fontSize: '24px'
          }}
          onClick={() => setSelectedMarker({ ...stop, position: stop.location })}
        />
      ))}

      {fuelStops?.map((stop, index) => (
        <Marker
          key={`fuel-${index}`}
          position={stop.geometry.location}
          label={{
            text: '⛽',
            fontSize: '24px'
          }}
          onClick={() => setSelectedMarker({ 
            ...stop, 
            position: stop.geometry.location,
            type: 'fuel'
          })}
        />
      ))}

      {selectedMarker && (
        <InfoWindow
          position={selectedMarker.position}
          onCloseClick={() => setSelectedMarker(null)}
        >
          <div>
            <h3>{selectedMarker.type.toUpperCase()}</h3>
            {selectedMarker.duration && (
              <p>Duration: {selectedMarker.duration} hours</p>
            )}
            {selectedMarker.start_time && (
              <p>Time: {selectedMarker.start_time} - {selectedMarker.end_time}</p>
            )}
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
};

export default Map;