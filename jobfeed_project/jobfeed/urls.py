from django.urls import path
from .views import JobFeedView

urlpatterns = [
    path('job-feed/', JobFeedView.as_view(), name='job_feed'),
]