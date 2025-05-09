import { useState } from 'react';
import { Container, Paper, Typography, Box, CircularProgress, Alert } from '@mui/material';
import { useLoadScript } from '@react-google-maps/api';
import RouteForm from '../components/RouteForm';
import Map from '../components/Map';
import LogSheet from '../components/LogSheet';
import { calculateRoute } from './services/api';

import { LinkedIn, GitHub, Email } from '@mui/icons-material';
import { IconButton, Tooltip, Link as MuiLink } from '@mui/material';

const libraries = ['places'];

function App() {
  // google Maps loading state
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

  // handle Google Maps loading states
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
      <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <Typography variant="h4" gutterBottom align="center">
          Route Planner & Log Generator
        </Typography>

        <Paper sx={{ 
          mb: 3, 
          p: 2, 
          maxWidth: "600px", 
          width: "100%" 
        }}>
          <RouteForm onSubmit={handleSubmit} />
        </Paper>

        {loading && (
          <Box display="flex" justifyContent="center" my={4} width="100%">
            <CircularProgress />
          </Box>
        )}

        {error && (
          <Box sx={{ maxWidth: "600px", width: "100%" }}>
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          </Box>
        )}

        {routeData && (
          <Box sx={{ maxWidth: "600px", width: "100%" }}>
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
          </Box>
        )}
          <Paper sx={{ 
            mt: 4, 
            p: 2, 
            maxWidth: '600px', 
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}>
            <Typography variant="h6" gutterBottom>
              Connect With Me
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Tooltip title="LinkedIn">
                <IconButton 
                  component={MuiLink} 
                  href="https://www.linkedin.com/in/abdeljalil-ouafi-8036a7266/" 
                  target="_blank"
                  color="primary"
                  aria-label="LinkedIn"
                >
                  <LinkedIn fontSize="large" />
                </IconButton>
              </Tooltip>
              
              <Tooltip title="GitHub">
                <IconButton 
                  component={MuiLink} 
                  href="https://github.com/AbdeljalilOuafi" 
                  target="_blank"
                  color="primary"
                  aria-label="GitHub"
                >
                  <GitHub fontSize="large" />
                </IconButton>
              </Tooltip>
              
              <Tooltip title="Email">
                <IconButton 
                  component={MuiLink} 
                  href="mailto:cv.ouafiabdeljalil@gmail.com" 
                  color="primary"
                  aria-label="Email"
                >
                  <Email fontSize="large" />
                </IconButton>
              </Tooltip>
            </Box>
          </Paper>
      </Box>
    </Container>
  );
}

export default App;