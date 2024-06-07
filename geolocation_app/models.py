from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    password = models.CharField(max_length=128, default='default_password')

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.timestamp}:  {self.user.username}: {self.message}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.TextField(null=True)

    def __str__(self):
        return self.user.username

class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    phone_number = models.TextField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.user.username
