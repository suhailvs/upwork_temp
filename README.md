# Deployment
+ Install Apache
```
$ apt-get update
$ apt-get install python-pip apache2 libapache2-mod-wsgi
```

+ Change dir: `$ cd /var/www/`
+ Clone the repo: `$ git clone https://github.com/suhailvs/upwork_temp`
+ Change dir: `$ cd upwork_temp`
+ Create virtual and install django:
```
$ pip install virtualenv
$ virtualenv env
$ source ./env/bin/activate
$ pip install django
```
+ Migrate and sync db and give permission to media:
```
$ mkdir media
$ chmod 777 media
$ ./manage.py makemigrations
$ ./manage.py migrate
$ cd media/
$ chmod 777 db.sqlite3
```

+ Edit apache config :

```
$ vi /etc/apache2/sites-enabled/000-default.conf

WSGIDaemonProcess sampleapp python-path=/var/www/upwork_temp:/var/www/upwork_temp/env/lib/python2.7/site-packages
WSGIProcessGroup sampleapp
WSGIScriptAlias / /var/www/upwork_temp/sampleapp/wsgi.py

```
+ restart apache: `service apache2 reload`

# Celery Installation

+ Install Rabbitmq:
```
$ echo 'deb http://www.rabbitmq.com/debian/ testing main' |
     sudo tee /etc/apt/sources.list.d/rabbitmq.list
$ apt-get update
$ apt-get install rabbitmq-server
```

+ Install Celery
`pip install celery`

+ Add file `sampleapp/sampleapp/celery.py`:
```
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleapp.settings')

app = Celery('sampleapp')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```
+ update `sampleapp/sampleapp/__init__.py`:
```
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']
```
+ starting the worker process
`celery -A sampleapp worker -l info -B`
+ create `uploader/tasks.py`:
```
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

```

+ Daemonization
here is a [nice tutorial](https://medium.com/@yehandjoe/celery-4-periodic-task-in-django-9f6b5a8c21c7)

`$ apt-get install supervisor`

Then, add `/etc/supervisor/conf.d/celery_proj_worker.conf` file:
```
; ==================================
; celery worker supervisor example
; ==================================
; the name of your supervisord program
[program:projworker]
; Set full path to celery program if using virtualenv
command=/var/www/upwork_temp/env/bin/celery -A sampleapp worker -l info
; The directory to your Django project
directory=/var/www/upwork_temp
; If supervisord is run as the root user, switch users to this UNIX user account before doing any processing.
; user=me
; Supervisor will start as many instances of this program as named by numprocs
numprocs=1
; Put process stdout output in this file stdout_logfile=/var/log/celery/proj_worker.log
; Put process stderr output in this file stderr_logfile=/var/log/celery/proj_worker.log
; If true, this program will start automatically when supervisord is started
autostart=true
; May be one of false, unexpected, or true. If false, the process will never be autorestarted. If unexpected, the process will be restart when the program exits with an exit code that is not one of the exit codes associated with this process’ configuration (see exitcodes). If true, the process will be unconditionally restarted when it exits, without regard to its exit code.
autorestart=true
; The total number of seconds which the program needs to stay running after a startup to consider the start successful.
startsecs=10
; Need to wait for currently executing tasks to finish at shutdown. ; Increase this if you have very long running tasks.
stopwaitsecs = 600 
; When resorting to send SIGKILL to the program to terminate it ; send SIGKILL to its whole process group instead, taking care of its children as well.
killasgroup=true
; if your broker is supervised, set its priority higher so it starts first
priority=998
```

Also add `/etc/supervisor/conf.d/celery_proj_beat.conf` file:
```
; ================================
;  celery beat supervisor example
; ================================
; the name of your supervisord program
[program:projbeat]
; Set full path to celery program if using virtualenv
command=/var/www/upwork_temp/env/bin/celery -A sampleapp beat -l info
; The directory to your Django project
directory=/var/www/upwork_temp
; If supervisord is run as the root user, switch users to this UNIX user account before doing any processing.
;user=me
; Supervisor will start as many instances of this program as named by numprocs
numprocs=1
; Put process stdout output in this file stdout_logfile=/var/log/celery/proj_beat.log
; Put process stderr output in this file stderr_logfile=/var/log/celery/proj_beat.log
; If true, this program will start automatically when supervisord is started
autostart=true
; May be one of false, unexpected, or true. If false, the process will never be autorestarted. If unexpected, the process will be restart when the program exits with an exit code that is not one of the exit codes associated with this process’ configuration (see exitcodes). If true, the process will be unconditionally restarted when it exits, without regard to its exit code.
autorestart=true
; The total number of seconds which the program needs to stay running after a startup to consider the start successful.
startsecs=10
; if your broker is supervised, set its priority higher so it starts first
priority=999
```

create empty log files:

```
$ touch /var/log/celery/proj_worker.log
$ touch /var/log/celery/proj_beat.log
```
update change for supervisor:
```
$ supervisorctl reread
$ supervisorctl update
```

Finally we can `start/stop/restart` the services or even check the status:
```
$ supervisorctl start projworker
$ supervisorctl stop projworker
$ supervisorctl restart projworker
$ supervisorctl status projworker

$ supervisorctl start projbeat
$ supervisorctl stop projbeat
$ supervisorctl restart projbeat
$ supervisorctl status projbeat
```

checkout log in:
`$ /var/log/supervisor`
