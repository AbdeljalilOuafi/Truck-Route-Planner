#!/usr/bin/env python3
"""google_maps_service module"""

import googlemaps
from django.conf import settings
from typing import Dict, List, Any

class GoogleMapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    def get_route_details(self, origin: Dict, destination: Dict, waypoints: List[Dict] = None) -> Dict[str, Any]:
        try:
            directions = self.client.directions(
                origin=f"{origin['lat']},{origin['lng']}",
                destination=f"{destination['lat']},{destination['lng']}",
                waypoints=[f"{wp['lat']},{wp['lng']}" for wp in (waypoints or [])],
                optimize_waypoints=True
            )

            if not directions:
                raise ValueError("No route found")

            route = directions[0]
            return {
                'distance': route['legs'][0]['distance']['value'],  # in meters
                'duration': route['legs'][0]['duration']['value'],  # in seconds
                'polyline': route['overview_polyline']['points'],
                'steps': route['legs'][0]['steps']
            }
        except Exception as e:
            raise Exception(f"Error calculating route: {str(e)}")

    def find_fuel_stops(self, route_points: List[Dict], max_distance: int = 1000000) -> List[Dict]:
        fuel_stops = []
        for point in route_points:
            places = self.client.places_nearby(
                location=(point['lat'], point['lng']),
                radius=5000,
                type='gas_station'
            )
            if places.get('results'):
                fuel_stops.append(places['results'][0])
        return fuel_stops