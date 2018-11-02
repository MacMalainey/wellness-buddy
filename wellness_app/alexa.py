from django_alexa.api import fields, intent, ResponseBuilder
from .processes import getCompliment, getTip
from .models import Tip


@intent
def LaunchRequest(session):
    """
    ---
    launch
    start
    run
    begin
    open
    """
    return ResponseBuilder.create_response(message= 'Hello!, I am your wellness buddy!', reprompt='what can I help you with?',end_session = False, launched= True)

class rateSlots(fields.AmazonSlots):
    rate = fields.AmazonNumber()


@intent(slots= rateSlots, app="OTHER")
def Start(session, rate):
    kwargs = {}
    kwargs['message'] = 'DEBUG MESSAGE'
    kwargs ['end_session'] = True
    kwargs ['launched'] = session['launched']
    return ResponseBuilder.create_response(**kwargs)

@intent(app="OTHER")
def Compliment(session):
    """
    ---
    give me a compliment
    give me a pick me up
    can i have some words of encouragement
    could i please have a pick me up
    """
    return ResponseBuilder.create_response(message= getCompliment().message, 
        end_session = True, launched= session['launched'])

@intent(app="OTHER")
def WellnessTips(session):
    return ResponseBuilder.create_response(message= getTip(Tip.LEVEL_MEDIUM).message, 
    end_session = True, launched= session['launched'])