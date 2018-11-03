# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from .processes import *
from .models import Tip

def alexa_ask(request):
    info = {}
    # response = responseTemplate()
    if info['request'] == "LaunchRequest":
        pass
    else:
        if info['intentName'] == 'Compliments':
            message = getCompliment()
        elif info['intentName'] == 'WellnessTip':
            message = getTip(Tip.LEVEL_MEDIUM)
        elif info['intentName'] == 'Start':
            user = getOrNewUser(info['userId'])
            data = decodeData(user.wellness_record[-3::-1])
        elif info['intentName'] == 'AMAZON.FallbackIntent':
            pass
            