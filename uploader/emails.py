from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.template import Context
from uploader.models import User

SITE_URL= 'http://minttalent.mooo.com'
from_email='support@minttalent.com'

def email_user(usr):
    email_dec = """
        Please Visit {0}/user/{1}/ 
        and Upload your profile picture.

        Thanks
        Mint Talent
        """.format(SITE_URL,usr.pk)
    EmailMessage('Please Upload your Image', 
            email_dec, to=[usr.email], from_email=from_email).send()
    
def email_candidate(c):
    ctx = {
        'candidate_name': c.firstname+' ' +c.lastname,
        'client_name': c.employer,
        'static_url': SITE_URL + '/static/' ,
        'user_image': SITE_URL + "/static/emails/hanna.png",
    }
    usr= User.objects.filter(uId=c.recruiter)
    if usr: 
        usr=usr[0]
        ctx['consultant_name'] = usr.firstname+ ' '+usr.lastname
        ctx['user_image']= SITE_URL+usr.pic.url
    message = get_template('emails/index.html').render(context=ctx)
    msg = EmailMessage('Welcome to MintTalent', message, from_email=from_email,to=[c.email] )
    if usr: msg.bcc=[usr.email]
    msg.content_subtype = 'html'
    msg.send()
