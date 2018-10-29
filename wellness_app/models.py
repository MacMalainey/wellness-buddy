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

class Compliment(models.Model):

    message = models.CharField()

class Tip(models.Model):

    message = models.CharField()

    # Constants for levels of mood
    # Ordered by quality of mood in ascending order
    LEVEL_CRITICAL = 0
    LEVEL_LOW = 1
    LEVEL_MEDIUM = 2
    LEVEL_GOOD = 3
    LEVEL_NONE = 4

    LEVEL_CHOICES = (
        (LEVEL_CRITICAL, 'CRITICAL'),
        (LEVEL_LOW, 'LOW'),
        (LEVEL_MEDIUM, 'MEDIUM'),
        (LEVEL_GOOD, 'GOOD'),
        (LEVEL_NONE, 'NONE')
    )

    level = models.SmallIntegerField(choices=LEVEL_CHOICES, null=False)