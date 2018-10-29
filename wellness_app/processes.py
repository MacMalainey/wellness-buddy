# -*- coding: utf-8 -*-

from .models import UserInfo
import statistics as stat
import math

def getResponseType(data):

    # If it was a 0 day it is automatically critical
    if(data[0] < 2):
        return Response(Response.LEVEL_CRITICAL)

    daysStored = len(data)

    if daysStored < 5:
        return Response(Response.LEVEL_NONE)
    
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
            return Response(Response.LEVEL_NONE)
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
        deviation_month = None
    
    # Start assigning response objects
    # 0-3 is a poor,
    # 4-6 is a medium/mixed
    # 7-9 is a high

    if deviation_week > 4:
            # Base it soley on today's value
            if data[0] < 4:
                return Response(Response.LEVEL_LOW)
            elif data[0] < 7:
                return Response(Response.LEVEL_MEDIUM)
            else:
                return Response(Response.LEVEL_GOOD)

    if mean_3 is None:
        if data[0] < 4 and mean_week < 4 and mean_month > 7:
            return Response(Response.LEVEL_CRITICAL)
        elif data[0] < 4:
            return Response(Response.LEVEL_LOW)
        elif mean_week < 7:
            return Response(Response.LEVEL_MEDIUM)
        else:
            return Response(Response.LEVEL_GOOD)
    else:
        if deviation_week > 4:
            # Base it soley on today's value
            if data[0] < 4:
                return Response(Response.LEVEL_LOW)
            elif data[0] < 7:
                return Response(Response.LEVEL_MEDIUM)
            else:
                return Response(Response.LEVEL_GOOD)
        elif data[0] < 4 and (mean_3 < 4 and (mean_month > 7 or mean_week > 7)):
            return Response(Response.LEVEL_CRITICAL)
        elif data[0] < 4:
            return Response(Response.LEVEL_LOW)
        elif mean_week < 7:
            return Response(Response.LEVEL_MEDIUM)
        else:
            return Response(Response.LEVEL_GOOD)





def appendDataToAccount(day, userId):
    try:
        user = UserInfo.objects.get(pk=userId)
        lastDay = int(user.wellness_record[-1])
        if lastDay > 16:
            user.wellness_record = user.wellness_record + encodeData(day)
        else:
            user.wellness_record = user.wellness_record + encodeData(day, base=ord(lastDay))
    except UserInfo.DoesNotExist:
        user = UserInfo(user_id=userId, data=encodeData(day))
    
    user.save()

# data = decodeData(user.wellness_record[-math.ceil(31/2)::-1])

def encodeData(data, base=None):
    if data is None:
        data = 0xA
    if base is not None:
        data = data << 4
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

            
class Response:

    # Constants for levels of mood
    # Ordered by quality of mood in ascending order
    LEVEL_CRITICAL = "CRITICAL"
    LEVEL_LOW = "LOW"
    LEVEL_MEDIUM = "MEDIUM"
    LEVEL_GOOD = "GOOD"
    LEVEL_NONE = "NONE"

    # NOTE this data algorithm SUCKS because this scale assumes everyone's average (5) is the same
    # in terms of data this fails drastically to truly reach the people who are depressed because it
    # assumes that they will always respond 1-3 which may not be the case.

    # A better algorithm would be to have a benchmark number for each person to measure around as their being "good"

    def __init__(self, suggested):
        self.suggested = suggested