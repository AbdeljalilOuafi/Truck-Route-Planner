from rest_framework import serializers
from .models import Route

class RouteInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['current_location', 'pickup_location', 
                 'dropoff_location', 'current_cycle_hours']

class RouteOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'