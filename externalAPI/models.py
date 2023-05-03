from django.db import models
from customUser.models import MyUser

class Publication(models.Model):
    manager = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
    body = models.TextField(blank=False)
    title = models.CharField(max_length=60, unique=True)
    isAvailable = models.BooleanField(default=True, blank=True)
    addingDate = models.DateField(auto_now_add=True)
    numberOfDownloads = models.IntegerField(default=0, blank=True)