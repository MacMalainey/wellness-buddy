from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import AlexaUser
import datetime
from .processes import appendDataToUserObject

@shared_task
def nullDay():
    print("Adding null input to all users who have no posted today")
    time = datetime.time(datetime.datetime.now().hour)
    userObjects = AlexaUser.objects.filter(time_zone=time, has_updated=False)
    for user in userObjects:
        appendDataToUserObject(0xA, user)
    
    for user in AlexaUser.objects.filter(time_zone=time, has_updated=True):
        user.has_update=False
        user.save()
    
