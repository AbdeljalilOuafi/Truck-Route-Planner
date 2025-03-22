# routes/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.google_maps_service import GoogleMapsService
from .services.hos_service import HOSCalculator
from .serializers import RouteInputSerializer, RouteOutputSerializer
from .services.log_generator import LogSheetGenerator
import datetime

@api_view(['POST'])
def calculate_route(request):
    serializer = RouteInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Initialize services
        maps_service = GoogleMapsService()
        hos_calculator = HOSCalculator(
            current_cycle_hours=serializer.validated_data['current_cycle_hours']
        )

        # Get route details
        route_details = maps_service.get_route_details(
            origin=serializer.validated_data['current_location'],
            destination=serializer.validated_data['dropoff_location'],
            waypoints=[serializer.validated_data['pickup_location']]
        )

        # Calculate driving hours and breaks
        total_drive_time = route_details['duration'] / 3600  # convert seconds to hours since route_details['duration'] is in seconds
        breaks = hos_calculator.calculate_breaks(total_drive_time)

        # Find fuel stops
        fuel_stops = maps_service.find_fuel_stops(
            route_points=[
                serializer.validated_data['current_location'],
                serializer.validated_data['pickup_location'],
                serializer.validated_data['dropoff_location']
            ]
        )
        
        # generate log sheets
        log_generator = LogSheetGenerator()
        log_sheets = log_generator.generate_daily_logs(
            breaks=breaks,
            start_time=datetime.datetime.now()
        )

        response_data = {
            **route_details,
            'breaks': breaks,
            'fuel_stops': fuel_stops,
            'total_trip_duration': total_drive_time + len([b for b in breaks if b['type'] in ['pickup', 'dropoff', 'break']]),
            'hos_compliance': total_drive_time <= hos_calculator.remaining_cycle_hours,
            'log_sheets': log_sheets
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Something went wrong, are you sure all the locations are valid and your API keys are in .env?, anyway here is the error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )