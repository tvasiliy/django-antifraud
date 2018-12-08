from django.urls import path
from . import views


urlpatterns = [
    path('torlist/', views.ListTorView.as_view(), name="torlist-all"),
    path('antifraud_history/', views.ListHistoryView.as_view(), name="history"),
    path('check_device/', views.check_device, name="check_device")
]
