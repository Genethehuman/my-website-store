from django.db import models

# Create your models here.

class MarketingMessage(models.Model):
    message = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)


    def __str__(self):
        return str(self.message)
