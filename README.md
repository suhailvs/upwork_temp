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
$ ./manage.py makemigrations
$ ./manage.py migrate

$ mkdir media
$ chmod 777 media
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
