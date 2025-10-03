# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add custom fields here
    email = models.EmailField(unique=True)
    address = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.username



# Optional: Category table for dropdown
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # when book added

    def __str__(self):
        return self.title   

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Using string for category
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    



    from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Bookshow(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='books/')
    
    def __str__(self):
        return self.title
