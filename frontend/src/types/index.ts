export interface Location {
    lat: number;
    lng: number;
    address?: string;
  }
  
  export interface RouteInput {
    current_location: Location;
    pickup_location: Location;
    dropoff_location: Location;
    current_cycle_hours: number;
  }
  
  export interface Break {
    type: string;
    duration: number;
    start_time: string;
    end_time: string;
    location?: string;
  }
  
  export interface LogSheet {
    date: string;
    activities: Break[];
    total_hours: number;
  }