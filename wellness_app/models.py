# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# User Information Model
# Stores specfic user input for learning
class AlexaUser(models.Model):
    
    # Amazon user ID, needed to store the aata specific to a user.
    user_id = models.CharField(max_length=255, primary_key=True)

    wellness_record = models.TextField()

class Compliment(models.Model):

    message = models.TextField()

    def __str__(self):
        return self.message[:30]

class Tip(models.Model):
    
    message = models.TextField()

    # Constants for levels of mood
    # Ordered by quality of mood in ascending order
    LEVEL_CRITICAL = 'CRITICAL'
    LEVEL_LOW = 'LOW'
    LEVEL_MEDIUM = 'MEDIUM'
    LEVEL_GOOD = 'GOOD'
    LEVEL_NONE = 'NONE'

    LEVEL_CHOICES = (
        (LEVEL_CRITICAL, 'CRITICAL'),
        (LEVEL_LOW, 'LOW'),
        (LEVEL_MEDIUM, 'MEDIUM'),
        (LEVEL_GOOD, 'GOOD'),
        (LEVEL_NONE, 'NONE')
    )

    level = models.CharField(choices=LEVEL_CHOICES, null=False, max_length=8)

    def __str__(self):
        return self.message[:30] + "  Level: " + self.level