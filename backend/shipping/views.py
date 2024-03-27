from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cargo, Truck
from .serializers import (CargoListSerializer,
                          CargoCreateSerializer,
                          CargoDetailSerializer,
                          TruckSerializer,
                          TruckUpdateSerializer)

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CargoDetailSerializer
        elif self.action == 'create':
            return CargoCreateSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CargoDetailSerializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = CargoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TruckUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        zip_code = serializer.validated_data['zip_code']

        if instance.update_location_from_zip_code(zip_code):
            return Response(serializer.data)
        else:
            return Response({"message": "Failed to update location."}, status=status.HTTP_400_BAD_REQUEST)
