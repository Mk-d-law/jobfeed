# jobfeed/views.py

from django.http import HttpResponse
from django.views.generic import View
from .models import Job
from django.utils.feedgenerator import Rss201rev2Feed

class JobFeedRSS(Rss201rev2Feed):
    title = "Job Feed"
    link = "/job-feed/"
    description = "Latest job listings"

    def items(self):
        return Job.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

class JobFeedView(View):
    def get(self, request):
        feed = JobFeedRSS()
        response = HttpResponse(content_type='application/rss+xml')
        feed.write(response, 'utf-8')
        return response
