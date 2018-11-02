<<<<<<< HEAD
@intent
def LaunchRequest(session):
    return ResponseBuilder.create_response(message= 'Hello!, I am your wellness buddy!', reprompt='what can I help you with?',end_session = False, launched= True)

class rateSlots(fields.AmazonSlots);
    rate = fields.AmazonCustom(label= "list_of_numbers")
    mood = fields.AmazonCustom(label = 'list_of_moods')


@intent(slots= rateSlots)
def start(session, rate, tip):
    if session.get('launched'):
        kwargs['message'] = 'How do you feel from one to ten"
        //how do i insert a the number that is spoken and push it into the database
        kwargs ['reprompt'] = Tip
        kwargs ['end_session'] = False
        kwargs ['launched'] = session['launched']
    return ResponseBuilder.create_response(**kwargs)

@intent
def compliments(session)
    if session.get('launched'):
        return ResponseBuilder.create_response(message= Compliment(), reprompt= 'Is there anything else I can help you with?', end_session = False, launched= True)

@intent
def tips(session)
    if session.get('launched'):
        return ResponseBuilder.create_response(message= getTip(), reprompt= 'Is there anything else I can help you with?', end_session = False, launched= True)






=======
from django_alexa.api import fields, intent, ResponseBuilder
from wellness_app.processes import *
>>>>>>> abb9d41ad061e69ac98fd9b580b0dc04206ee66d
