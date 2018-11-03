# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
import json
from .processes import getOrNewUser, getCompliment, getTip, decodeData, appendDataToUserObject, response_template, getResponseType, parseRequest
from .models import Tip

def alexa_ask(request):
    response = response_template()
    info = parseRequest(request.POST)
    # response = responseTemplate()
    if info['request'] == "LaunchRequest":
        response['shouldEndSession'] = False
        response['response']['outputSpeech']['text'] = "Hello."
        response['reprompt'] = {
            "outputSpeech": {
                "type": "PlainText",
                "text": "What can I help you with?"
            }
        }
    else:
        if info['intentName'] == 'Compliments':
            response['response']['outputSpeech']['text'] = getCompliment().message
        elif info['intentName'] == 'WellnessTip':
            response['message'] = getTip(Tip.LEVEL_MEDIUM)
        elif info['intentName'] == 'Start':
            user = getOrNewUser(info['userId'])
            data = decodeData(user.wellness_record[-1, -2])
            data.insert(0, info['rate'])
            response['response']['outputSpeech']['text'] = getTip(getResponseType(data)).message
            appendDataToUserObject(info['rate'], user)
        elif info['intentName'] == 'AMAZON.FallbackIntent':
            response['response']['outputSpeech']['text'] = "Sorry I can't help you with that."
            response['reprompt'] = {
				"outputSpeech": {
					"type": "PlainText",
					"text": "What can I help you with?"
				}
			}
    
    return JsonResponse(response)