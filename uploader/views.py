# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from uploader.models import UploadForm,UserEmail

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
# Create your views here.
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
def home(request):
	if request.method=="POST":
		try:
			validate_email(request.POST.get("email", ""))
		except ValidationError as e:
			#print "oops! wrong email"
			return HttpResponse('''<h1> Invalid email</h1>
				Please provide xx@ss.xx format email. Thanks''')
		else:
			#print "hooray! email is valid"

			usr= UserEmail(email=request.POST['email'])
			usr.save()

			email_dec = """
			Please Visit http://suhailvs.mooo.com/user/{0}/ 
			and Upload your profile picture.

			Thanks
			This is just a test
			""".format(usr.pk)

			send_mail('Please Upload your Image', 
				email_dec,
				'suhailvs@gmail.com',[usr.email],fail_silently=False)
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
			#'file saved'
			return HttpResponseRedirect(reverse('user_pic',args=[pk]))
	else:
		img=UploadForm()
	return render(request,'upload.html',{'form':img,'user':usr})
		
	
		