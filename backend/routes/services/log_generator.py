#!/usr/bin/env python3
"""log_generator module"""


from datetime import datetime, timedelta
from typing import List, Dict
import re   #this is regex btw
import googlemaps
from django.conf import settings

class LogSheetGenerator:
    def __init__(self):
        self.STATUS_CODES = {
            'driving': 'D',
            'break': 'SB',
            'pickup': 'ON',
            'dropoff': 'ON',
            'off_duty': 'OFF',
            'fuel': 'ON'
        }
        self.maps_client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    def extract_route_waypoints(self, route_info: Dict) -> List[Dict]:
        """Extract meaningful waypoints from the route with proper distances"""
        waypoints = []
        total_distance = 0
        
        # Add starting point
        waypoints.append({
            'name': route_info['locations']['current'].get('address'),
            'distance': 0
        })

        # Process steps directly from route_details
        for step in route_info['route_details']['steps']:
            total_distance += step['distance']['value']
            
            # Only add significant points (steps with substantial distance)
            if step['distance']['value'] > 50000:  # More than 50km
                try:
                    result = self.maps_client.reverse_geocode((
                        step['end_location']['lat'],
                        step['end_location']['lng']
                    ))[0]
                    
                    locality = ""
                    state = ""
                    for component in result['address_components']:
                        if 'locality' in component['types']:
                            locality = component['long_name']
                        elif 'administrative_area_level_1' in component['types']:
                            state = component['short_name']
                    
                    if locality and state:
                        waypoints.append({
                            'name': f"{locality}, {state}",
                            'distance': round(total_distance / 1609.34, 1)  # Convert to miles
                        })
                except Exception as e:
                    print(f"Error in geocoding: {str(e)}")
                    continue

        # Add destination point
        waypoints.append({
            'name': route_info['locations']['dropoff'].get('address'),
            'distance': round(route_info['route_details']['distance'] / 1609.34, 1)
        })

        return waypoints

    def get_location_at_progress(self, progress_miles: float, waypoints: List[Dict]) -> Dict:
        """Get current and next location based on distance traveled"""
        for i in range(len(waypoints) - 1):
            current = waypoints[i]
            next_point = waypoints[i + 1]
            
            if progress_miles >= current['distance'] and progress_miles <= next_point['distance']:
                return {
                    'current': current,
                    'next': next_point
                }
        return None

    def get_location_description(self, activity: Dict, route_info: Dict, waypoints: List[Dict]) -> str:
        """Generate meaningful location descriptions based on activity type and progress"""
        if activity['type'] == 'pickup':
            return f"Pickup at {route_info['locations']['pickup'].get('address')}"
        elif activity['type'] == 'dropoff':
            return f"Dropoff at {route_info['locations']['dropoff'].get('address')}"

        total_duration = route_info['route_details']['duration']
        total_distance = route_info['route_details']['distance'] / 1609.34  # Convert to miles
        
        # Calculate progress
        progress_miles = (activity['start_time'] * 3600 / total_duration) * total_distance
        location_info = self.get_location_at_progress(progress_miles, waypoints)
        
        if not location_info:
            return "En Route"

        if activity['type'] == 'driving':
            return f"Driving from {location_info['current']['name']} to {location_info['next']['name']}"
        elif activity['type'] == 'break':
            return f"Rest Stop near {location_info['current']['name']} ({round(progress_miles, 1)} miles from start)"
        elif activity['type'] == 'fuel':
            return f"Refueling near {location_info['current']['name']} ({round(progress_miles, 1)} miles from start)"
        
        return "En Route"

    def generate_daily_logs(self, breaks: List[Dict], start_time: datetime, route_info: Dict) -> List[Dict]:
        # Extract waypoints from the actual route
        waypoints = self.extract_route_waypoints(route_info)
        
        daily_logs = []
        current_time = start_time
        current_day_activities = []
        
        for activity in breaks:
            activity_start = current_time + timedelta(hours=activity['start_time'])
            activity_end = current_time + timedelta(hours=activity['end_time'])
            
            while activity_start.date() != activity_end.date():
                midnight = activity_start.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                duration_until_midnight = (midnight - activity_start).total_seconds() / 3600
                
                current_day_activities.append({
                    'status': self.STATUS_CODES[activity['type']],
                    'start_time': activity_start.strftime('%H:%M'),
                    'end_time': '24:00',
                    'duration': duration_until_midnight,
                    'location': self.get_location_description(activity, route_info, waypoints)
                })
                
                daily_logs.append({
                    'date': activity_start.strftime('%Y-%m-%d'),
                    'activities': current_day_activities.copy(),
                    'total_hours': sum(a['duration'] for a in current_day_activities)
                })
                
                current_day_activities = []
                activity_start = midnight
                
            current_day_activities.append({
                'status': self.STATUS_CODES[activity['type']],
                'start_time': activity_start.strftime('%H:%M'),
                'end_time': activity_end.strftime('%H:%M'),
                'duration': activity['duration'],
                'location': self.get_location_description(activity, route_info, waypoints)
            })
            
            if activity == breaks[-1]:
                daily_logs.append({
                    'date': activity_start.strftime('%Y-%m-%d'),
                    'activities': current_day_activities.copy(),
                    'total_hours': sum(a['duration'] for a in current_day_activities)
                })
                
        return daily_logs