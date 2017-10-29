# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from uploader.models import Candidate,User,Synclog
from uploader.emails import email_user, email_candidate
import urllib2,json

def api_request(endpoint):	
	api_key="Bearer c89a75b73fc1a4753d9fa4a0361e3e49"
	api_url="https://api.jobadder.com/v2"+endpoint
	req = urllib2.Request(api_url)
	req.add_header('Authorization',api_key)
	resp=urllib2.urlopen(req)	
	return json.loads(resp.read())

def sync_users():
	data = api_request('/users')
	for u in data['items']:
		if User.objects.filter(uId=u['userId']):continue
		usr= User(uId=u['userId'],firstname=u['firstName'],
			lastname=u['lastName'],email=u['email'])
		usr.save()
		#email_user(usr)

def sync_candidates():
	data = api_request('/candidates')
	for c in data['items']:
		c_id=c['candidateId']
		status = c['status']['name']
		if status not in ['Placed (PERM)','Placed (CONTRACT)']: continue
		if Candidate.objects.filter(cId=c_id):continue
		
		d2 = api_request('/candidates/'+str(c_id))
		cand = Candidate(cId=c['candidateId'],firstname=c['firstName'],
			lastname=c['lastName'],email=c['email'],
			recruiter=d2['recruiters'][0]['userId'])
		if 'employment' in d2:
			cand.employer=d2["employment"]['current']['employer']
		cand.save()
		#email_candidate(cand)		
	
@shared_task
def sync_api():
	slog=Synclog.objects.create() #status = 'fail'
	sync_users()
	slog.status='cfail'
	slog.save()

	sync_candidates()
	slog.status='success'
	slog.save()
