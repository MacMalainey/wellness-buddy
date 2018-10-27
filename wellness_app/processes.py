# -*- coding: utf-8 -*-

from .models import UserInfo
import statistics as stat
import math

def getResponseType(userId):
    try:
        user = UserInfo.objects.get(pk=userId)
        # Because the last character of the string corresponds to the
        # most recent day the string needs to be reversed and cut at the end

        
        data = decodeDataString(user.wellness_record[-math.ceil(31/2)::-1])
        mean_3 = stat.mean(data[0:3])
        mean_week = stat.mean(data[0:7])
        deviation_week = stat.pvariance(data, mu=mean_week)
    except UserInfo.DoesNotExist:
        return ResponseType()


def decodeDataString(data):
    data = []
    # Loop through each hex value
    for character in map(int, data):
        for x in [0, 1]:
            bits = character[4*x:4*(x+1)]
            hx = bits.hex
            if hx > 0x0 and hx < 0x9:
                data.append(int(hx))
            elif hx == 0xA:
                data.append(None)
            else:
                # TODO HANDLE MORE SPECIAL CASE CHARACTERS LATER
                data.append(None)

    return data

            
class ResponseType:

    # Constants for levels of mood
    # Ordered by quality of mood in ascending order
    LEVEL_POOR = "POOR"
    LEVEL_LOW = "LOW"
    LEVEL_MIXED = "MIXED"
    LEVEL_MEDIUM = "MEDIUM"
    LEVEL_GOOD = "GOOD"
    LEVEL_NONE = "NONE"

    def __init__(self, month=LEVEL_NONE, week=LEVEL_NONE, average=LEVEL_NONE, suggested=LEVEL_NONE):
        self.month = month
        self.week = week
        self.average = average
        self.suggested = suggested