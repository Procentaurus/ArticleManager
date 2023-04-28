from django.db import models

from customUser.models import MyUser

class Project(models.Model):
    name = models.CharField(max_length=40, unique=True)
    manager = models.OneToOneField(MyUser,related_name='manager', on_delete=models.SET_NULL, null=True)
    writers = models.ManyToManyField(MyUser,related_name='writers')
    startDate = models.DateField(auto_now_add=True)
    isFinished = models.BooleanField(default=False)

    def __string__(self):
        return self.name

class Text(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(max_length=2000, null=False)
    creationDate = models.DateField(auto_now_add=True)
    lastModified =  models.DateField(auto_now=True)

    class Meta:
        ordering = ["-creationDate", "author"]


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    body = models.TextField(max_length=300, null=False)
    creationDate = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["-creationDate", "author"]


