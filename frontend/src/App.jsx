import { useState } from 'react';
import { Container, Paper, Typography, Box, CircularProgress, Alert } from '@mui/material';
import { useLoadScript } from '@react-google-maps/api';
import RouteForm from '../components/RouteForm';
import Map from '../components/Map';
import LogSheet from '../components/LogSheet';
import { calculateRoute } from './services/api';

// Define libraries array at the top level
const libraries = ['places'];

function App() {
  // Google Maps loading state
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [routeData, setRouteData] = useState(null);

  const handleSubmit = async (formData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await calculateRoute(formData);
      setRouteData(response);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Handle Google Maps loading states
  if (loadError) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">
          Error loading Google Maps: Please check your API key and enabled services
        </Alert>
      </Container>
    );
  }

  if (!isLoaded) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Route Planner & Log Generator
      </Typography>

      <Paper sx={{ mb: 3, p: 2 }}>
        <RouteForm onSubmit={handleSubmit} />
      </Paper>

      {loading && (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {routeData && (
        <>
          <Paper sx={{ mb: 3, p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Route Map
            </Typography>
            <Map 
              route={routeData}
              stops={routeData.breaks}
              fuelStops={routeData.fuel_stops}
            />
          </Paper>

          <Paper sx={{ mb: 3, p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Trip Summary
            </Typography>
            <Typography>
              Total Trip Duration: {routeData.total_trip_duration.toFixed(2)} hours
            </Typography>
            <Typography>
              HOS Compliance: {routeData.hos_compliance ? '✅ Compliant' : '❌ Non-compliant'}
            </Typography>
          </Paper>

          <LogSheet logSheets={routeData.log_sheets} />
        </>
      )}
    </Container>
  );
}

export default App;