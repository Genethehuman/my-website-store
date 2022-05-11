from django.urls import reverse
from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'zhopki'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-details', kwargs={"pizda": self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
            all_objects = Post.objects.all()
            for i in all_objects:
                if self.slug == i.slug:
                    self.slug += str(self.id)
            # if self.slug in all_objects.slug:
            #     self.slug = self.slug + self.id


        super().save(*args, **kwargs)
                
    

