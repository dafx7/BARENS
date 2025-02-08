from django.urls import path
from .views import kelola_penghuni, toggle_status_penghuni

urlpatterns = [
    path("pengelolaan-akun/", kelola_penghuni, name="kelola_penghuni"),
    path("toggle-status/<int:user_id>/", toggle_status_penghuni, name="toggle_status_penghuni"),
]
