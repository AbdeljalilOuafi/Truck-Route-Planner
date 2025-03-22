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

    def generate_daily_logs(self, breaks: List[Dict], start_time: datetime) -> List[Dict]:
        daily_logs = []
        current_time = start_time
        current_day_activities = []
        
        for activity in breaks:
            activity_start = current_time + timedelta(hours=activity['start_time'])
            activity_end = current_time + timedelta(hours=activity['end_time'])
            
            # If activity crosses midnight, split it
            while activity_start.date() != activity_end.date():
                # Create log entry until midnight
                midnight = activity_start.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                duration_until_midnight = (midnight - activity_start).total_seconds() / 3600
                
                current_day_activities.append({
                    'status': self.STATUS_CODES[activity['type']],
                    'start_time': activity_start.strftime('%H:%M'),
                    'end_time': '24:00',
                    'duration': duration_until_midnight,
                    'location': activity.get('location', 'En Route')
                })
                
                # Add completed day to logs
                daily_logs.append({
                    'date': activity_start.strftime('%Y-%m-%d'),
                    'activities': current_day_activities.copy(),
                    'total_hours': sum(a['duration'] for a in current_day_activities)
                })
                
                # Reset for next day
                current_day_activities = []
                activity_start = midnight
                
            # Add final/single day activity
            current_day_activities.append({
                'status': self.STATUS_CODES[activity['type']],
                'start_time': activity_start.strftime('%H:%M'),
                'end_time': activity_end.strftime('%H:%M'),
                'duration': activity['duration'],
                'location': activity.get('location', 'En Route')
            })
            
            # If this is the last activity or next activity is on different day
            if activity == breaks[-1]:
                daily_logs.append({
                    'date': activity_start.strftime('%Y-%m-%d'),
                    'activities': current_day_activities.copy(),
                    'total_hours': sum(a['duration'] for a in current_day_activities)
                })
                
        return daily_logs