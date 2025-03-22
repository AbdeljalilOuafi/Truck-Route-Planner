from django.db import models

class Route(models.Model):
    current_location = models.JSONField()
    pickup_location = models.JSONField()
    dropoff_location = models.JSONField()
    current_cycle_hours = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # these are calculated data for the route that's displayed as a map on the frontend
    estimated_duration = models.FloatField(null=True)
    route_polyline = models.TextField(null=True)
    stops = models.JSONField(null=True)