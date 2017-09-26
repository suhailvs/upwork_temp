# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from uploader.models import UploadForm,UserEmail

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.
def home(request):
	if request.method=="POST":
		usr= UserEmail(email=request.POST['email'])
		usr.save()
		return HttpResponseRedirect(reverse('home'))
	
	users=UserEmail.objects.all()
	return render(request,'home.html',{'users':users})

def upload(request,pk):
	usr=UserEmail.objects.get(pk=pk)
	if usr.pic:
		# if pic exist. show the pic
		return render(request,'view.html',{'user':usr})

	# if pic doesnt exist. show the fileupload
	if request.method=="POST":
		# if post create the pic
		img = UploadForm(request.FILES)		
		if img.is_valid():
			usr.pic = request.FILES['pic']
			usr.save()	
			print 'file saved'
			return HttpResponseRedirect(reverse('user_pic',args=[pk]))
	else:
		img=UploadForm()
	return render(request,'upload.html',{'form':img})
		
	
		