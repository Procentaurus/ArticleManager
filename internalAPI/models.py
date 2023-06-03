from uuid import uuid4
from django.db import models

from customUser.models import MyUser

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=80, unique=True)
    manager = models.OneToOneField(MyUser,related_name='manager', on_delete=models.SET_NULL, null=True)
    writers = models.ManyToManyField(MyUser,related_name='writers')
    startDate = models.DateField()
    isFinished = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    body = models.TextField(blank=False)
    creationDate = models.DateField(auto_now_add=True)
    lastModified =  models.DateField(auto_now=True)

    class Meta:
        ordering = ["-creationDate", "author"]


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    body = models.TextField(max_length=500, null=False)
    creationDate = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["-creationDate", "author"]


