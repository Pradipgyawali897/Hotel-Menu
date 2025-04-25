from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=12, validators=[MaxLengthValidator(12)])
    ID = models.IntegerField(unique=True, blank=False, primary_key=True)
    availability = models.BooleanField(default=True)
    date_created = models.DateField(auto_now=True)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f"{self.name} (ID: {self.ID})"