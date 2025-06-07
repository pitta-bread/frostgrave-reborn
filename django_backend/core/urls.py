from django.urls import path
from .api import api

urlpatterns = [
    path("api/", api.urls),  # Include the API URLs from NinjaExtraAPI
]
