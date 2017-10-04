# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from uploader.models import Candidate,User

@shared_task
def add(x, y):
    return x + y

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

from uploader.emails import email_user, email_candidate

@shared_task
def sync_users():
	data = api_request('/users')
	for u in data['items']:
		if User.objects.filter(uId=u['userId']):continue
		usr= User(uId=u['userId'],firstname=u['firstName'],
			lastname=u['lastName'],email=u['email'])
		usr.save()
		email_user(usr)

@shared_task
def sync_candidates():
	data = api_request('/candidates')
	for c in data['items']:
		c_id=c['candidateId']
		if Candidate.objects.filter(cId=c_id):continue
		d2 = api_request('/candidates/'+str(c_id))
		cand = Candidate(cId=c['candidateId'],firstname=c['firstName'],
			lastname=c['lastName'],email=c['email'],
			recruiter=d2['recruiters'][0]['userId'])
		if 'employment' in d2:
			cand.employer=d2["employment"]['current']['employer']
		cand.save()
		email_candidate(cand)		
	
