from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('sendTemperature/', views.TemperatureView.as_view(), name='send_temperature'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]