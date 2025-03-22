// src/App.jsx
import { useState } from 'react';
import { 
  Box, 
  CircularProgress, 
  TextField, 
  Button 
} from '@mui/material';
import { useLoadScript, Autocomplete } from '@react-google-maps/api';

// RouteForm component included in the same file for clarity
const libraries = ['places'];

const RouteForm = ({ onSubmit }) => {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries
  });

  const [formData, setFormData] = useState({
    current_location: null,
    pickup_location: null,
    dropoff_location: null,
    current_cycle_hours: 0
  });

  const handlePlaceSelect = (place, field) => {
    if (place.geometry) {
      setFormData(prev => ({
        ...prev,
        [field]: {
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng(),
          address: place.formatted_address
        }
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.current_location && formData.pickup_location && formData.dropoff_location) {
      onSubmit(formData);
    }
  };

  if (!isLoaded) return <CircularProgress />;

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ p: 2 }}>
      <Autocomplete
        onLoad={autocomplete => {
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            handlePlaceSelect(place, 'current_location');
          });
        }}
      >
        <TextField
          fullWidth
          label="Current Location"
          margin="normal"
          required
        />
      </Autocomplete>

      <Autocomplete
        onLoad={autocomplete => {
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            handlePlaceSelect(place, 'pickup_location');
          });
        }}
      >
        <TextField
          fullWidth
          label="Pickup Location"
          margin="normal"
          required
        />
      </Autocomplete>

      <Autocomplete
        onLoad={autocomplete => {
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            handlePlaceSelect(place, 'dropoff_location');
          });
        }}
      >
        <TextField
          fullWidth
          label="Dropoff Location"
          margin="normal"
          required
        />
      </Autocomplete>

      <TextField
        fullWidth
        type="number"
        label="Current Cycle Hours"
        margin="normal"
        required
        value={formData.current_cycle_hours}
        onChange={(e) => setFormData({
          ...formData,
          current_cycle_hours: parseFloat(e.target.value)
        })}
        inputProps={{ min: 0, max: 70, step: 0.5 }}
      />

      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        sx={{ mt: 2 }}
        disabled={!formData.current_location || !formData.pickup_location || !formData.dropoff_location}
      >
        Calculate Route
      </Button>
    </Box>
  );
};

export default RouteForm