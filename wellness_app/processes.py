# -*- coding: utf-8 -*-

from .models import AlexaUser, Tip
import statistics as stat
import math
import random

def getResponseType(data):

    # If it was a 0 day it is automatically critical
    if(data[0] < 2):
        return getTip(Tip.LEVEL_CRITICAL)

    daysStored = len(data)

    if daysStored < 5:
        return getTip(Tip.LEVEL_NONE)
    
    processable = []

    # Get the data for the most recent three days
    # These have the greatest emphasis on the ouput of this function
    for element in data[0:3]:
        if element is not None:
            processable.append(element)

    if len(processable) > 1:
        # Get the average for the last 3 days
        mean_3 = stat.mean(processable[0:3])
    else:
        # If not enough data set value to None to indicate this
        mean_3 = None
    

    # Get the data for the week
    for element in data[4:7]:
        if element is not None:
            processable.append(element)
    
    if len(processable) > 5:
        # Get the mean for the last week
        mean_week = stat.mean(processable[0:7])
        deviation_week = stat.pvariance(data, mu=mean_week)
    else:
        if(mean_3 is None):
            return getTip(Tip.LEVEL_NONE)
        else:
            mean_week = None
            deviation_week = None

    # Get the rest of the data for the rest of the month
    for element in data[8:31]:
        if element is not None:
            processable.append(element)
    
    if len(processable) > 20:
        mean_month = stat.mean(processable[0:31])
    else:
        mean_month = None
    
    # Start assigning response objects
    # 0-3 is a poor,
    # 4-6 is a medium/mixed
    # 7-9 is a high

    if deviation_week > 4:
            # Base it soley on today's value
            if data[0] < 4:
                return getTip(Tip.LEVEL_LOW)
            elif data[0] < 7:
                return getTip(Tip.LEVEL_MEDIUM)
            else:
                return getTip(Tip.LEVEL_GOOD)

    if mean_3 is None:
        if data[0] < 4 and mean_week < 4 and mean_month > 7:
            return getTip(Tip.LEVEL_CRITICAL)
        elif data[0] < 4:
            return getTip(Tip.LEVEL_LOW)
        elif mean_week < 7:
            return getTip(Tip.LEVEL_MEDIUM)
        else:
            return getTip(Tip.LEVEL_GOOD)
    else:
        if deviation_week > 4:
            # Base it soley on today's value
            if data[0] < 4:
                return getTip(Tip.LEVEL_LOW)
            elif data[0] < 7:
                return getTip(Tip.LEVEL_MEDIUM)
            else:
                return getTip(Tip.LEVEL_GOOD)
        elif data[0] < 4 and (mean_3 < 4 and (mean_month > 7 or mean_week > 7)):
            return getTip(Tip.LEVEL_CRITICAL)
        elif data[0] < 4:
            return getTip(Tip.LEVEL_LOW)
        elif mean_week < 7:
            return getTip(Tip.LEVEL_MEDIUM)
        else:
            return getTip(Tip.LEVEL_GOOD)




# Appends data to a uuser with the given userId, if no user exists it will create a new user.
def appendDataToAccount(day, userId):
    try:
        user = AlexaUser.objects.get(pk=userId)
        lastDay = int(user.wellness_record[-1])
        if lastDay > 16:
            user.wellness_record = user.wellness_record + encodeData(day)
        else:
            user.wellness_record = user.wellness_record + encodeData(day, base=ord(lastDay))
    except AlexaUser.DoesNotExist:
        user = AlexaUser(user_id=userId, data=encodeData(day))
    
    user.save()
    return user

# Appends data to a known user that for sure exists in the database (i.e. pulled already)
def appendDataToUserObject(day, user):
    lastDay = int(user.wellness_record[-1])
    if lastDay > 16:
        user.wellness_record = user.wellness_record + encodeData(day)
    else:
        user.wellness_record = user.wellness_record + encodeData(day, base=ord(lastDay))
    
    user.save()

# data = decodeData(user.wellness_record[-math.ceil(31/2)::-1])

def encodeData(data, base=-1):
    if data > 0xF:
        data = 0xA
    elif data is None:
        data = 0xA
    
    if base != -1:
        data = data << 4
        if base > 0xF:
            base = 0xA
        elif base is None:
            base = 0xA
        return chr(data + base)
    else:
        return chr(data)


    

def decodeData(data):
    res = []
    # Loop through each hex value
    for character in map(ord, data):
        if character < 0x1F:
            if character > 0x0 and character < 0x9:
                res.append(int(character))
            elif character == 0xA:
                res.append(None)
            else:
                # TODO HANDLE MORE SPECIAL CASE CHARACTERS LATER
                res.append(None)
        else:
            for x in [1, 0]:
                hx = (character & (0b1111 << (4*x))) >> (4*x)
                if hx > 0x0 and hx < 0x9:
                    res.append(int(hx))
                elif hx == 0xA:
                    res.append(None)
                else:
                    # TODO HANDLE MORE SPECIAL CASE CHARACTERS LATER
                    res.append(None)
    return res

            
def getTip(tip_level):
    tips = Tip.objects.filter(level=tip_level)
    max_tip_index = len(tips)
    return tips[random.randint(0, max_tip_index)].message
