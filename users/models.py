from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    '''
    This model is used to store additional information about the user.
    '''
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    address = models.CharField(verbose_name = "Address",max_length=100, blank=True, null=True)
    town = models.CharField(verbose_name = "Town/City",max_length=100, blank=True, null=True)
    county = models.CharField(verbose_name = "County",max_length=100, blank=True, null=True)
    post_code = models.CharField(verbose_name = "Post code",max_length=8, blank=True, null=True)
    country = models.CharField(verbose_name = "Country",max_length=100, blank=True, null=True)
    longitude = models.CharField(verbose_name = "Longitude",max_length=50, blank=True, null=True)
    lattitude = models.CharField(verbose_name = "Lattitude",max_length=50, blank=True, null=True)

    captcha_score = models.FloatField(default=0.0)
    has_profile = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'