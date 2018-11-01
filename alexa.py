<<<<<<< HEAD
def getWelcomeResponse(callback)
    speechOutput = 'Hello, I'm your wellness buddy!'
    repromptText = 'How can I help you today?'
    shouldEndSession = false
    callback(sessionAttributes, buildSpeechletResponse(speechOutput, repromptText, shouldEndSession))

def onIntent(intentRequest, session, callback)
    console.log(`onIntent requestId=${intentRequest.requestId}, sessionId=${session.sessionId}`)
    intent = intentRequest.intent
    intentName = intentRequest.intent.name


    if (intentName === 'AMAZON.HelpIntent')
        getWelcomeResponse(callback):
    else if (intentName === 'AMAZON.StopIntent')
        handleSessionEndRequest(callback):
    else if (intentName === 'Start')
        getStartResponse(callback):


=======
from django_alexa.api import fields, intent, ResponseBuilder
from wellness_app.processes import *
>>>>>>> abb9d41ad061e69ac98fd9b580b0dc04206ee66d
