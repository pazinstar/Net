from django.db import models
from django.utils import timezone

class UserBalance(models.Model):
    username = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
   
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def days_until_expiry(self):
        if self.expiry_date:
            return max(0, (self.expiry_date - timezone.now()).days)
        return None
from django.db import models

class AdminList(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # You should use a hashed password in a real-world scenario

    def __str__(self):
        return self.username
