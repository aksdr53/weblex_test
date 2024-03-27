from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargoViewSet, TruckViewSet


router = DefaultRouter()


router.register(r'cargos', CargoViewSet)
router.register(r'trucks', TruckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]