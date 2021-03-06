# Deployment
+ Install Apache
```
$ apt-get update
$ apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
```

+ Change dir: `$ cd /var/www/`
+ Clone the repo: `$ git clone https://github.com/suhailvs/upwork_temp`
+ Change dir: `$ cd upwork_temp`
+ Create virtual and install django:
```
$ pip3 install virtualenv
$ virtualenv env
$ source ./env/bin/activate
$ pip install django
$ pip install celery
```
+ Migrate and sync db and give permission to media:
```
$ mkdir media
$ chmod 777 media
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py loaddata users.json
$ cd media/
$ chmod 777 db.sqlite3
```

+ Edit apache config :

```
$ vi /etc/apache2/sites-available/upwork_temp.conf

<VirtualHost *:80>
    ServerName ng.helpservice.xyz

    WSGIDaemonProcess upworkapp python-home=/var/www/upwork_temp/env python-path=/var/www/upwork_temp
    WSGIProcessGroup upworkapp
    WSGIScriptAlias / /var/www/upwork_temp/sampleapp/wsgi.py
    ErrorLog /var/www/upwork_temp/error.log
    CustomLog /var/www/upwork_temp/access.log combined
</VirtualHost>

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


# lets encrypt for HTTPS

https://github.com/certbot/certbot/issues/1820

I had to comment the `WSGIDaemonProcess` line out before running letsencrypt. 

in `/etc/apache2/sites-available/upwork_temp.conf`::

    <VirtualHost *:80>
        ServerName ng.helpservice.xyz

        # WSGIDaemonProcess upworkapp python-home=/var/www/upwork_temp/env python-path=/var/www/upwork_temp


https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-16-04

    apt-get install python3-certbot-apache
    certbot --apache -d example.com -d www.example.com

Then uncommented `WSGIDaemonProcess`.
