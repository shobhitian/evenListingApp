
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('1', 'pending'),
        ('2', 'approved'),
        ('3', 'suspended'),
       
     
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f"{self.first_name} {self.last_name} (DOB: {self.dob}, Phone: {self.phone_number}, Address: {self.address}, Image: {self.image})"

