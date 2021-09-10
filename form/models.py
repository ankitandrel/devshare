from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Submit_Resource(models.Model):
    resource_name = models.CharField(max_length=200)
    resource_category = models.CharField(max_length=200)
    resource_link = models.URLField(max_length=10000, unique=True)
    resource_info = models.TextField()
    resource_submited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submited_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resource_name

    class Meta:
        verbose_name = 'Submit Resource'
        verbose_name_plural = 'Submit Resource'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    social_media_handle = models.URLField(max_length=2000)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_on_date = models.DateTimeField(auto_now=True)
    contact_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} is contacting about {self.subject}"
