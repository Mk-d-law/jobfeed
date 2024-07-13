from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from xml.etree.ElementTree import Element, SubElement, tostring

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def generate_xml_feed():
    jobs = Job.objects.all()
    root = Element('jobfeed')

    for job in jobs:
        job_elem = SubElement(root, 'job')
        SubElement(job_elem, 'title').text = job.title
        SubElement(job_elem, 'company').text = job.company
        SubElement(job_elem, 'location').text = job.location
        SubElement(job_elem, 'description').text = job.description
        SubElement(job_elem, 'date_posted').text = job.date_posted.strftime('%Y-%m-%d')

    xml_string = tostring(root, encoding='utf-8')
    with open('jobfeed.xml', 'wb') as f:
        f.write(xml_string)

@receiver(post_save, sender=Job)
def update_xml_feed(sender, instance, created, **kwargs):
    if created:
        print(f"Job created: {instance.title}, updating XML feed.")
        generate_xml_feed()
