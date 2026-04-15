from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/predict/', views.PredictAPIView.as_view(), name='api_predict'),
]