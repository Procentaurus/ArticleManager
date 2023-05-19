from uuid import uuid4
from django.db import models
from django.core.validators import MinLengthValidator

from customUser.models import MyUser

class Publication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    manager = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
    body = models.TextField(blank=False)
    title = models.CharField(max_length=80, unique=True, validators=[MinLengthValidator(8)])
    isAvailable = models.BooleanField(default=True, blank=True)
    addingDate = models.DateField(auto_now_add=True)
    numberOfDownloads = models.IntegerField(default=0, blank=True)