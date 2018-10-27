# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# User Information Model
# Stores specfic user input for learning
class UserInfo(models.Model):
    
    # Amazon user ID, needed to store the aata specific to a user.
    user_id = models.CharField(max_length=255, primary_key=True)

    wellness_record = models.CharField()

    long_term_record = models.FileField(upload_to='archived_records/')