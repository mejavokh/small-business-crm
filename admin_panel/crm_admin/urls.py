from django.urls import path
from .views import statistics_view

urlpatterns = [
    path('my_statics', statistics_view)
]