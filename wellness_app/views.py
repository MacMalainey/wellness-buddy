# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
import json
from .processes import getOrNewUser, getCompliment, getTip, decodeData, appendDataToUserObject, response_template, getResponseType, parseRequest
from .models import Tip

def alexa_ask(request):
    response = response_template()
    info = parseRequest(json.loads(request.body))

    if info['intentType'] == "LaunchRequest":
        response['shouldEndSession'] = False
        response['response']['outputSpeech']['text'] = "Hello."
        response['reprompt'] = {
            "outputSpeech": {
                "type": "PlainText",
                "text": "What can I help you with?"
            }
        }
    elif info['intentType'] == "IntentRequest":
        if info['name'] == 'Compliment':
            response['response']['outputSpeech']['text'] = getCompliment().message
        elif info['name'] == 'WellnessTips':
            response['response']['outputSpeech']['text'] = getTip(Tip.LEVEL_MEDIUM).message
        elif info['name'] == 'Start':
            user = getOrNewUser(info['userId'])
            data = decodeData(user.wellness_record[-1: -2])
            data.insert(0, int(info['rate']))
            response['response']['outputSpeech']['text'] = getResponseType(data).message
            appendDataToUserObject(int(info['rate']), user)
        elif info['name'] == 'AMAZON.FallbackIntent':
            response['response']['outputSpeech']['text'] = "Sorry I can't help you with that."
            response['reprompt'] = {
				"outputSpeech": {
					"type": "PlainText",
					"text": "What can I help you with?"
				}
			}
    
    return JsonResponse(response)