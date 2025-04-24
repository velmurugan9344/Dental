# models.py
from django.db import models

class Appointment(models.Model):
    service = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email