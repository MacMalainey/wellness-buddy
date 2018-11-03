# -*- coding: utf-8 -*-

from .models import AlexaUser, Tip, Compliment
import statistics as stat
import math
import random

def getResponseType(data):

    # If it was a 0 day it is automatically critical
    if(data[0] < 3):
        return getTip(Tip.LEVEL_CRITICAL)

    processable = []

    # Get the data for the most recent three days
    # These have the greatest emphasis on the ouput of this function
    for element in data[0:3]:
        if element is not None:
            processable.append(element)

    if len(processable) == 3:
        # Get the average for the last 3 days
        mean_3 = stat.mean(processable)
    elif len(processable) == 1:
        return getTip(Tip.LEVEL_NONE)
    else:
        # If not enough data set value to None to indicate this
        mean_3 = None

    # Start assigning response objects
    # 0-3 is a poor,
    # 4-6 is a medium/mixed
    # 7-9 is a high
    if data[0] < 4 and mean_3 > 4.5:
        return getTip(Tip.LEVEL_CRITICAL)
    elif data[0] < 5:
        return getTip(Tip.LEVEL_LOW)
    elif data[0] < 8:
        return getTip(Tip.LEVEL_MEDIUM)
    else:
        return getTip(Tip.LEVEL_GOOD)




# Pulls the user with the given userId, if no user exists it will create a new user.
def getOrNewUser(userId):
    try:
        user = AlexaUser.objects.get(pk=userId)
    except AlexaUser.DoesNotExist:
        user = AlexaUser.objects.create(user_id=userId, wellness_record="")
        user.save()
    return user

# Appends data to a known user that for sure exists in the database (i.e. pulled already)
def appendDataToUserObject(day, user):
    if(len(user.wellness_record) > 0):
        lastDay = user.wellness_record[-1]
        if ord(lastDay) > 0xF:
            user.wellness_record = user.wellness_record + encodeData(day)
        else:
            user.wellness_record = user.wellness_record + encodeData(day, base=ord(lastDay))
    else:
        user.wellness_record = user.wellness_record + encodeData(day)

    user.save()

def encodeData(data, base=-1):
    if data > 0xF:
        data = 0xB
    elif data is None:
        data = 0xB

    if base != -1:
        data = data << 4
        if base > 0xF:
            base = 0xB
        elif base is None:
            base = 0xB
        return chr(data + base)
    else:
        return chr(data)




def decodeData(data):
    res = []
    # Loop through each hex value
    for character in map(ord, data):
        if character < 0x10:
            if character > 0x0 and character <= 0xA:
                res.append(int(character))
            elif character == 0xB:
                res.append(None)
            else:
                # TODO HANDLE MORE SPECIAL CASE CHARACTERS LATER
                res.append(None)
        else:
            for x in [1, 0]:
                hx = (character & (0b1111 << (4*x))) >> (4*x)
                if hx > 0x0 and hx <= 0xA:
                    res.append(int(hx))
                elif hx == 0xB:
                    res.append(None)
                else:
                    # TODO HANDLE MORE SPECIAL CASE CHARACTERS LATER
                    res.append(None)
    return res


def getTip(tip_level):
    tips = Tip.objects.filter(level=tip_level)
    max_tip_index = len(tips)
    if len(max_tip_index == 1):
        return tips[0]
    return tips[random.randint(0, max_tip_index - 1)]


def getCompliment():
    comp = Compliment.objects.all()
    max_comp_index = len(comp)
    return comp[random.randint(0, max_comp_index - 1)]


def response_template():
    response_dict = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": ""
            },
        },
    }

    return response_dict


def parseRequest(postRequest):
    request = {
        "userId": postRequest["session"]['user']["userId"],
        "intentType": postRequest["request"]["type"]
    }

    if postRequest["request"]["type"] == "IntentRequest":
        request["name"] = postRequest["request"]["intent"]["name"]
        if postRequest["request"]["intent"]["name"] == "Start":
            request["rate"] = postRequest["request"]["intent"]["slots"]["rate"]["value"]

    return request

