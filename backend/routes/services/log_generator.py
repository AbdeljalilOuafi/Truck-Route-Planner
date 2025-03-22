#!/usr/bin/env python3
"""log_generator module"""


from datetime import datetime, timedelta
from typing import List, Dict

class LogSheetGenerator:
    def __init__(self):
        self.STATUS_CODES = {
            'driving': 'D',
            'break': 'SB',
            'pickup': 'ON',
            'dropoff': 'ON',
            'off_duty': 'OFF'
        }

    def format_address(self, address: str) -> str:
        """Format the Google Maps address to be more concise"""
        if not address:
            return "En Route"
        
        # Split address into components
        parts = address.split(', ')
        
        # If we have a full address, return just city and state
        if len(parts) >= 2:
            city = parts[0]
            state = parts[1]
            return f"{city}, {state}"
        
        return address

    def get_location_description(self, activity: Dict, route_info: Dict) -> str:
        """Generate meaningful location descriptions based on activity type"""
        locations = route_info['locations']
        
        if activity['type'] == 'pickup':
            return self.format_address(locations['pickup'].get('address'))
        elif activity['type'] == 'dropoff':
            return self.format_address(locations['dropoff'].get('address'))
        elif activity['type'] == 'driving':
            current = self.format_address(locations['current'].get('address'))
            dropoff = self.format_address(locations['dropoff'].get('address'))
            return f"En Route: {current} → {dropoff}"
        elif activity['type'] == 'break':
            current = self.format_address(locations['current'].get('address'))
            return f"Rest Stop near {current}"
        
        return self.format_address(activity.get('location', 'En Route'))

    def generate_daily_logs(self, breaks: List[Dict], start_time: datetime, route_info: Dict) -> List[Dict]:
        daily_logs = []
        current_time = start_time
        current_day_activities = []
        
        for activity in breaks:
            activity_start = current_time + timedelta(hours=activity['start_time'])
            activity_end = current_time + timedelta(hours=activity['end_time'])
            
            # If activity crosses midnight, split it
            while activity_start.date() != activity_end.date():
                midnight = activity_start.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                duration_until_midnight = (midnight - activity_start).total_seconds() / 3600
                
                current_day_activities.append({
                    'status': self.STATUS_CODES[activity['type']],
                    'start_time': activity_start.strftime('%H:%M'),
                    'end_time': '24:00',
                    'duration': duration_until_midnight,
                    'location': self.get_location_description(activity, route_info)
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
                'location': self.get_location_description(activity, route_info)
            })
            
            if activity == breaks[-1]:
                daily_logs.append({
                    'date': activity_start.strftime('%Y-%m-%d'),
                    'activities': current_day_activities.copy(),
                    'total_hours': sum(a['duration'] for a in current_day_activities)
                })
                
        return daily_logs