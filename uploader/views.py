# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from uploader.models import UploadForm,Candidate,User

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
# Create your views here.
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

def api_request(endpoint):
	import urllib2,json
	api_key="Bearer c89a75b73fc1a4753d9fa4a0361e3e49"
	api_url="http://api.jobadder.com/v2"+endpoint
	req = urllib2.Request(api_url)
	req.add_header('Authorization',api_key)
	try:
		resp=urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		print 'Http ERROR:'+str(err.code)
		raise

	return json.loads(resp.read())
"""
# sync emails

data = api_request('/candidates')

for c in data['items']:
	print c['email']
	if Candidate.objects.filter(email=c['email']):continue
	usr= Candidate(cId=c['candidateId'],firstname=c['firstName'],
	email=c['email'])
	
	data2 = api_request('/candidates/'+str(c['candidateId']))
	usr.recruiter=data2['recruiters'][0]['firstName']
	if 'employment' in data2:
		usr.employer=data2["employment"]['current']['employer']

	usr.save()
"""
def home(request):
	if request.method=="POST":
		# sync emails

		data = api_request('/users')
		
		for u in data['items']:
			if User.objects.filter(email=u['email']):continue
			usr= User(uId=u['userId'],firstname=u['firstName'],
			email=u['email'])
			usr.save()
		'''
		# email for image upload
		email_dec = """
		Please Visit http://suhailvs.mooo.com/user/{0}/ 
		and Upload your profile picture.

		Thanks
		This is just a test
		""".format(usr.pk)

		send_mail('Please Upload your Image', 
			email_dec,
			'support@minttalent.com',[usr.email],fail_silently=False)
		return HttpResponseRedirect(reverse('home'))
		'''
	users=User.objects.all()
	return render(request,'home.html',{'users':users})

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
