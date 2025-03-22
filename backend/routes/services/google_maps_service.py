#!/usr/bin/env python3
"""google_maps_service module"""

from django.conf import settings
from typing import Dict, List, Any
import googlemaps


class GoogleMapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


    def get_route_details(self, origin: Dict, destination: Dict, waypoints: List[Dict] = None) -> Dict[str, Any]:
        try:
            directions = self.client.directions(
                origin=f"{origin['lat']},{origin['lng']}",
                destination=f"{destination['lat']},{destination['lng']}",
                waypoints=[f"{wp['lat']},{wp['lng']}" for wp in (waypoints or [])],
                optimize_waypoints=True,
                # adding alternatives=True allows us to get multiple route options 
                alternatives=True
            )

            if not directions:
                raise ValueError("No route found")

            route = directions[0]
            
            # Calculate total distance and duration
            total_distance = sum(leg['distance']['value'] for leg in route['legs'])
            total_duration = sum(leg['duration']['value'] for leg in route['legs'])

            return {
                'distance': total_distance,  # in meters
                'duration': total_duration,  # in seconds
                'polyline': route['overview_polyline']['points'],
                'steps': route['legs'][0]['steps'],
                'bounds': route['bounds']
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