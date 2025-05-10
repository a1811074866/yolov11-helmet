from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    type=models.CharField(max_length=6,default='user')
    class Meta:
        db_table="user"

class Record(models.Model):
    name=models.CharField(max_length=1000)
    user_upload = models.CharField(max_length=100)
    created_at = models.CharField(max_length=100)
    with_helmet = models.CharField(max_length=100)
    without_helmet=models.CharField(max_length=100)

    class Meta:
        db_table="Record"


