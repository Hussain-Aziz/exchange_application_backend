from django.urls import path
from .views import (
    Comparison
)

urlpatterns = [
    path('comparison/', Comparison.as_view(), name='comparison'),
]

