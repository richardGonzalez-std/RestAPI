from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',null=True,blank=True)
    title = models.CharField(max_length=200)
    phone_number = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=True)
    def __str__(self):
        return self.title
# Create your models here.
