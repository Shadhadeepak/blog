from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    image_url=models.URLField( max_length=200,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(default="example-slug")
    category=models.ForeignKey('Category',  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title

# Catergory
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class AboutUs(models.Model):
    content=models.TextField()
