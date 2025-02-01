from django.urls import path
from .views import status_pembayaran

urlpatterns = [
    path("status-pembayaran/", status_pembayaran, name="status_pembayaran"),
]
