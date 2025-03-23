# 🚚 Truck Route Planner & ELD Logger

## 📋 Introduction

The Truck Route Planner & ELD Logger is a comprehensive web application designed to assist truck drivers and fleet managers in planning efficient routes while maintaining compliance with Hours of Service (HOS) regulations. The application automatically calculates optimal routes, schedules necessary breaks, plans fuel stops, and generates electronic logging device (ELD) compliant logs.

## ✨ Features

### Route Planning
- Real-time route calculation using Google Maps API
- Optimized waypoint routing
- Visual route display with interactive map
- Accurate distance and duration calculations
- Support for international routes

### HOS Compliance
- Automatic break scheduling based on HOS regulations
- 70-hour/8-day cycle tracking
- Mandatory rest period calculations
- Break location recommendations
- Real-time compliance monitoring

### Fuel Stop Planning
- Automatic fuel stop scheduling every 1,000 miles
- Integration with Google Places API for real gas station locations
- Rating-based gas station recommendations
- Detailed station information including:
  - Station name and address
  - Distance from route
  - Station ratings (when available)

### Electronic Logging
- Automatic generation of ELD-compliant log sheets
- Daily activity tracking including:
  - Driving periods
  - Rest breaks
  - Fuel stops
  - Loading/unloading times
- Detailed location tracking throughout the journey
- Multi-day trip support

### Interactive UI
- Simple, intuitive interface
- Real-time route visualization
- Detailed trip summary
- Visual log sheet display

## Technologies Used

### Frontend
- React (Vite)
- Material-UI
- @react-google-maps/api
- Axios
- TypeScript

### Backend
- Django
- Django REST Framework
- Python Google Maps Client
- Python-decouple

### APIs
- Google Maps JavaScript API
- Google Places API
- Google Directions API
- Google Geocoding API

## Getting Started

### 📋 Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- Google Cloud Platform account with enabled APIs
- API key with access to required Google services

### 💻 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/truck-route-planner.git
cd truck-route-planner
```

2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file, assuming you're still in the backend directory
touch  ../.env

# Add your Google Maps API key to .env and your Django Secret Key
echo "GOOGLE_MAPS_API_KEY=" > ../.env
echo "DJANGO_SECRET=" > ../.env

```

3. Frontend Setup
```bash
cd frontend
npm install

# Create .env file
touch .env

# Add your Google Maps API key to .env
echo "VITE_GOOGLE_MAPS_API_KEY=" > .env

```

### Configuration
1. Set up your Google Cloud Console project
2. Enable required APIs:
   - Maps JavaScript API
   - Places API
   - Directions API
   - Geocoding API
3. Create API credentials and add to both .env files

### Running the Application
1. Start the backend server
```bash
cd backend

# Run migrations
python manage.py migrate

# RUn server
python manage.py runserver
```

2. Start the frontend development server
```bash
cd frontend
npm run dev
```

3. Access the application at http://localhost:5173

## Contributors
- Abdeljalil Ouafi - Initial work and core functionality