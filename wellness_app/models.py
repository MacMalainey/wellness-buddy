# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserInfo(models.Model):
    
    # Amazon user ID, needed to store the aata specific to a user.
    user_id = models.CharField(max_length=255)

    wellness_record = models.CharField(max_length=62)

    long_term_record = models.FileField(upload_to='archived_records/')

    


    