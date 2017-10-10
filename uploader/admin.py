# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import User,Candidate,Synclog

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Synclog)
