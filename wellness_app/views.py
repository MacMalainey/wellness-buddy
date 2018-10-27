# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, SuspiciousOperation

from .models import UserInfo

# Create your views here.

def track_today(request):
    if request.method == 'POST':
        pass
    else:
        raise SuspiciousOperation
