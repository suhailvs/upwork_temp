# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm

class Candidate(models.Model):
	cId=models.CharField(max_length=10)
	email = models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	recruiter = models.CharField(max_length=50)
	employer = models.CharField(max_length=50)
	
	
class User(models.Model):
	uId=models.CharField(max_length=10)
	email=models.CharField(max_length=50)
	firstname=models.CharField(max_length=50)
	pic = models.FileField(upload_to="images/",blank=True,null=True)    
	upload_date=models.DateTimeField(auto_now_add =True)

# FileUpload form class.
class UploadForm(ModelForm):
	class Meta:
		model = User
		
		fields = ('pic',)