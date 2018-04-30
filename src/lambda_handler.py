

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" --- Main handler --- """
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
""" --- Intents --- """
def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))    #get the intent name

    intent_name = intent_request['currentIntent']['name']

    if intent_name= 'searchFood':
        return search_food(intent_request)
    raise Exception('Intent with name '+ intent_name + ' not supported')

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit,message):
    return {
        'sessionAttributes' : session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots':slots,
            'slotToElicit': slot_to_elicit,
            'message':message
        }
    }
def delegate(session_attributes,slots):
    return {
        'sessionAttributes' : session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
def close(session_attributes,fulfillment_state,message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction':{
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

def search_food(intent_request):
    #get slots from the intent
    source = intent_request['invocationSource']
    if source = 'DialogCodeHook':
        #basic validation on input slots
        slots = intent_request['currentIntent']['slots']
    return
