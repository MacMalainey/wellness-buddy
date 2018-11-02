from django_alexa.api import fields, intent, ResponseBuilder
from .processes import getCompliment, getTip
from .models import Tip


@intent
def LaunchRequest(session):
    return ResponseBuilder.create_response(message= 'Hello!, I am your wellness buddy!', reprompt='what can I help you with?',end_session = False, launched= True)

class rateSlots(fields.AmazonSlots):
    rate = fields.AmazonNumber()


@intent(slots= rateSlots)
def Start(session, rate):
    kwargs = {}
    kwargs['message'] = 'DEBUG MESSAGE'
    kwargs ['end_session'] = True
    kwargs ['launched'] = session['launched']
    return ResponseBuilder.create_response(**kwargs)

@intent
def Compliments(session):
    return ResponseBuilder.create_response(message= getCompliment().message, 
        end_session = True, launched= session['launched'])

@intent
def WellnessTips(session):
    return ResponseBuilder.create_response(message= getTip(Tip.LEVEL_MEDIUM).message, 
    end_session = True, launched= session['launched'])