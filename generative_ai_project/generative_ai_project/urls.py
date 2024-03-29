"""
URL configuration for generative_ai_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# myapp/urls.py
# GenerativeAi/urls.py
from django.contrib import admin
from django.urls import path, include
from code_evaluator.views import home, get_exercise
from django.urls import path
from code_evaluator.views import generate_and_evaluate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('code_evaluator.urls')),  # Include app-level URLs
    path('exercise/<int:exercise_id>/', get_exercise, name='get_exercise'),  # Add this line
    path('generate_and_evaluate', generate_and_evaluate, name='generate_and_evaluate'),

]
