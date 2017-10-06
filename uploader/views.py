# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from uploader.models import UploadForm,Candidate,User,Synclog

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

def home(request):	
	users=User.objects.order_by('-date')
	return render(request,'home.html',{'users':users})

def candidates(request):	
	cands=Candidate.objects.order_by('-date')
	return render(request,'candidates.html',{'cands':cands})

def sync_log(request):	
	slog=Synclog.objects.order_by('-date')
	return render(request,'logs.html',{'logs':slog})

def upload(request,pk):
	usr=User.objects.get(pk=pk)
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
			#'file saved'
			return HttpResponseRedirect(reverse('user_pic',args=[pk]))
	else:
		img=UploadForm()
	return render(request,'upload.html',{'form':img,'user':usr})
