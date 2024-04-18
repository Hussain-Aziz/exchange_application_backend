from django.urls import path
from .views import (
    Comparison,
    ComparisonOnApplication
)

urlpatterns = [
    # general get endpoint to comapare 2 pdf files via links (params: course_1, course_2)
    path('comparison/', Comparison.as_view(), name='comparison'),
    # get endpoint to do comparison for a course application (params: id)
    path('compare_application/', ComparisonOnApplication.as_view(), name='compare_application'),
]

