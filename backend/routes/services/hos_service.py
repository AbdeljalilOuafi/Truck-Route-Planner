from datetime import datetime, timedelta
from typing import List, Dict

class HOSCalculator:
    MAX_DRIVING_HOURS = 11
    MAX_DUTY_HOURS = 14
    MAX_CYCLE_HOURS = 70
    REQUIRED_BREAK_AFTER = 8
    MINIMUM_BREAK_DURATION = 0.5  # 30 minutes
    MILES_PER_FUEL_STOP = 1000  # miles
    FUELING_DURATION = 0.5  # 30 minutes
    
    
    def __init__(self, current_cycle_hours: float):
        self.current_cycle_hours = current_cycle_hours
        self.remaining_cycle_hours = self.MAX_CYCLE_HOURS - current_cycle_hours


    def calculate_breaks(self, total_drive_time: float, total_distance: float) -> List[Dict]:
        breaks = []
        current_drive_time = 0
        total_time = 0
        distance_covered = 0
        distance_since_fuel = 0
        
        # Add initial pickup
        breaks.append({
            'type': 'pickup',
            'duration': 1,
            'start_time': total_time,
            'end_time': total_time + 1,
            'distance_covered': distance_covered
        })
        total_time += 1
        
        while current_drive_time < total_drive_time:
            # Calculate next segment duration
            remaining_drive = min(
                self.REQUIRED_BREAK_AFTER,
                total_drive_time - current_drive_time,
                self.remaining_cycle_hours
            )
            
            # Calculate distance for this segment (proportional to driving time)
            segment_distance = (remaining_drive / total_drive_time) * total_distance
            
            # Check if we need a fuel stop within this segment
            if distance_since_fuel + segment_distance >= self.MILES_PER_FUEL_STOP:
                # Add driving until fuel stop
                distance_to_fuel = self.MILES_PER_FUEL_STOP - distance_since_fuel
                drive_time_to_fuel = (distance_to_fuel / total_distance) * total_drive_time
                
                if drive_time_to_fuel > 0:
                    breaks.append({
                        'type': 'driving',
                        'duration': drive_time_to_fuel,
                        'start_time': total_time,
                        'end_time': total_time + drive_time_to_fuel,
                        'distance_covered': distance_covered + distance_to_fuel
                    })
                    
                    total_time += drive_time_to_fuel
                    current_drive_time += drive_time_to_fuel
                    distance_covered += distance_to_fuel
                
                # Add fuel stop
                breaks.append({
                    'type': 'fuel',
                    'duration': self.FUELING_DURATION,
                    'start_time': total_time,
                    'end_time': total_time + self.FUELING_DURATION,
                    'distance_covered': distance_covered,
                    'route_percentage': (distance_covered / total_distance) * 100  # Add percentage along route
                })
                
                total_time += self.FUELING_DURATION
                distance_since_fuel = 0
                
                # Recalculate remaining segment
                remaining_distance = segment_distance - distance_to_fuel
                remaining_drive = (remaining_distance / total_distance) * total_drive_time
            
            # Add driving segment
            if remaining_drive > 0:
                segment_distance_remaining = (remaining_drive / total_drive_time) * total_distance
                
                breaks.append({
                    'type': 'driving',
                    'duration': remaining_drive,
                    'start_time': total_time,
                    'end_time': total_time + remaining_drive,
                    'distance_covered': distance_covered + segment_distance_remaining
                })
                
                total_time += remaining_drive
                current_drive_time += remaining_drive
                distance_covered += segment_distance_remaining
                distance_since_fuel += segment_distance_remaining
            
            # Add mandatory break if needed
            if current_drive_time < total_drive_time:
                breaks.append({
                    'type': 'break',
                    'duration': self.MINIMUM_BREAK_DURATION,
                    'start_time': total_time,
                    'end_time': total_time + self.MINIMUM_BREAK_DURATION,
                    'distance_covered': distance_covered
                })
                total_time += self.MINIMUM_BREAK_DURATION
        
        # Add final dropoff
        breaks.append({
            'type': 'dropoff',
            'duration': 1,
            'start_time': total_time,
            'end_time': total_time + 1,
            'distance_covered': distance_covered
        })
        
        # Debug print to see fuel stop distribution
        for idx, break_info in enumerate(breaks):
            if break_info['type'] == 'fuel':
                print(f"Fuel stop {idx}: at {break_info['distance_covered']:.1f} miles ({break_info['route_percentage']:.1f}% of route)")
        
        return breaks