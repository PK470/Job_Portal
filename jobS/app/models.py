from django.db import models
from django.contrib.auth.models import User
from django import forms



# Create your models here.
class Juser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='customer',null=True,blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    employer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Resume(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    linkdean = models.CharField(max_length=100, null=True)
    pdf = models.FileField(upload_to='resumes/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Job(models.Model):
    company = models.ForeignKey(Juser,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)
    j_description = models.CharField(max_length=1000,null=True)
    skills = models.CharField(max_length=200,null=True)
    offer = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=100,null=True)
    no_of_opening = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    
class Apply(models.Model):
    job = models.ForeignKey(Job,  on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
