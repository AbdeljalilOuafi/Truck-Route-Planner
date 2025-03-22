from datetime import datetime, timedelta
from typing import List, Dict

class HOSCalculator:
    MAX_DRIVING_HOURS = 11
    MAX_DUTY_HOURS = 14
    MAX_CYCLE_HOURS = 70
    REQUIRED_BREAK_AFTER = 8
    MINIMUM_BREAK_DURATION = 0.5  # 30 minutes

    def __init__(self, current_cycle_hours: float):
        self.current_cycle_hours = current_cycle_hours
        self.remaining_cycle_hours = self.MAX_CYCLE_HOURS - current_cycle_hours

    def calculate_breaks(self, total_drive_time: float) -> List[Dict]:
        breaks = []
        current_drive_time = 0
        total_time = 0

        # add initial pickup time
        breaks.append({
            'type': 'pickup',
            'duration': 1,  # 1 hour
            'location_type': 'pickup',
            'start_time': total_time,
            'end_time': total_time + 1
        })
        total_time += 1

        while current_drive_time < total_drive_time:
            # here we calculate the next driving segment
            remaining_drive = min(
                self.REQUIRED_BREAK_AFTER,
                total_drive_time - current_drive_time,
                self.remaining_cycle_hours
            )

            # Add driving period
            breaks.append({
                'type': 'driving',
                'duration': remaining_drive,
                'start_time': total_time,
                'end_time': total_time + remaining_drive
            })
            
            total_time += remaining_drive
            current_drive_time += remaining_drive
            self.remaining_cycle_hours -= remaining_drive

            # Add mandatory break if needed
            if current_drive_time < total_drive_time:
                breaks.append({
                    'type': 'break',
                    'duration': self.MINIMUM_BREAK_DURATION, # the value is in hours, not in minutes so 0.5 = 30 minutes
                    'start_time': total_time,
                    'end_time': total_time + self.MINIMUM_BREAK_DURATION
                })
                total_time += self.MINIMUM_BREAK_DURATION

        # Add final dropoff time
        breaks.append({
            'type': 'dropoff',
            'duration': 1,  # 1 hour
            'location_type': 'dropoff',
            'start_time': total_time,
            'end_time': total_time + 1
        })

        return breaks