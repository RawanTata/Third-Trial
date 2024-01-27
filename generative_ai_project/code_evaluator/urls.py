from django.urls import path
from .views import home  # Ensure this view is defined

urlpatterns = [
    path('', home, name='home'),  # Define a URL pattern for the home view
    # Add more URL patterns as needed
    
    
]
