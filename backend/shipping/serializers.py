from rest_framework import serializers
from .models import Location, Truck, Cargo
from .distance import calculate_distance

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

class CargoCreateSerializer(serializers.ModelSerializer):
    pick_up_zip = serializers.CharField(max_length=10)
    delivery_zip = serializers.CharField(max_length=10)

    class Meta:
        model = Cargo
        fields = ['pick_up_zip', 'delivery_zip', 'weight', 'description']

    def create(self, validated_data):
        pick_up_zip = validated_data.pop('pick_up_zip')
        delivery_zip = validated_data.pop('delivery_zip')

        # Геокодируем zip-коды для определения координат
        pick_up_location = Location.objects.filter(zip_code=pick_up_zip).first()
        delivery_location = Location.objects.filter(zip_code=delivery_zip).first()

        if not pick_up_location or not delivery_location:
            raise serializers.ValidationError("Invalid zip code(s)")

        validated_data['pick_up_location'] = pick_up_location
        validated_data['delivery_location'] = delivery_location

        return super().create(validated_data)


class CargoListSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()
    nearby_trucks_count = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_location', 'delivery_location', 'weight', 'description', 'nearby_trucks']

    def get_pick_up_location(self, obj):
        return obj.pick_up_location.city

    def get_delivery_location(self, obj):
        return obj.delivery_location.city

    def get_nearby_trucks(self, obj):
        cargo_pickup_location = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)
        nearby_trucks = []
        for truck in Truck.objects.all():
            truck_location = (truck.current_location.latitude, truck.current_location.longitude)
            distance = calculate_distance(truck_location, cargo_pickup_location)
            if distance <= 450:
                nearby_trucks.append({
                    'id': truck.id,
                    'current_location': {
                        'latitude': truck.current_location.latitude,
                        'longitude': truck.current_location.longitude
                    }
                })
        return nearby_trucks


class CargoDetailSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()
    trucks_with_distance = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_location', 'delivery_location', 'weight', 'description', 'trucks_with_distance']

    def get_pick_up_location(self, obj):
        return obj.pick_up_location.city

    def get_delivery_location(self, obj):
        return obj.delivery_location.city

    def get_trucks_with_distance(self, obj):
        cargo_pickup_location = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)
        trucks_with_distance = []
        for truck in Truck.objects.all():
            truck_location = (truck.current_location.latitude, truck.current_location.longitude)
            distance = calculate_distance(truck_location, cargo_pickup_location)
            trucks_with_distance.append({
                'truck_id': truck.id,
                'distance': distance
            })
        return trucks_with_distance


class TruckUpdateSerializer(serializers.Serializer):
    zip_code = serializers.CharField(max_length=10)  # Предполагается, что zip_code это строка
