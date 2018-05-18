import recipe as rc
import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" --- Main handler --- """
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    #logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
""" --- Intents --- """
def dispatch(intent_request):
    #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))    #get the intent name
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'getRecipe':
        return search_food(intent_request)
    elif intent_name == 'randomSuggestion':
        return random_food(intent_request)
    elif intent_name == 'getJoke':
        return get_joke(intent_request)
    raise Exception('Call my father! I do not know what '+ intent_name + ' means')

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

def parse_time(time_slot):
    return re.search("\d+",time_slot).group(0)

def random_food(intent_request):
    output_session_attributes = intent_request['sessionAttributes']
    #get slots from the intent
    source = intent_request['invocationSource']
    slots = get_slots(intent_request)
    if source == 'FulfillmentCodeHook':
        results = rc.getRandomRecipe()[0]
    response = "Here you go, my friend. This one is delicious \n"
    response += make_recipe_entry(results['title'],results['readyInMinutes'],results['sourceUrl'])
    return close(
    intent_request['sessionAttributes'],
    'Fulfilled',
    {
        'contentType' : 'PlainText',
        'content':response
    }
    )    

def make_recipe_entry(name,time,url):
    r = name + " \n " + "It takes about "+str(time)+" minutes to make.\n"
    r +="Full Recipe: "+url
    return r

def get_joke(intent_request):
    source = intent_request['invocationSource']
    results = "Hmm what? I think we are in different wavelengths my boi"
    if source == 'FulfillmentCodeHook':
        results = rc.getJoke()
    return close(
    intent_request['sessionAttributes'],
    'Fulfilled',
    {
        'contentType' : 'PlainText',
        'content':"One joke pulling right up ... \n" + results['text']
    }
    )
    
def make_steps(info, steps):
    response = "This deliciousness takes " +\
      str(info['readyInMinutes']) +\
      " minutes to make and serves "+\
      str(info['servings']) +" .\nFull Recipe available at " +\
      info['sourceUrl'] + ".\nHere are the steps:\n\n"
    if steps and steps[0]['steps']:
      for i, r_step in enumerate(steps[0]['steps']):
        equip_str = ""
        for e in r_step['equipment']:
          equip_str += e['name'] + ", "
        if not equip_str:
          equip_str = "None"
        else:
          equip_str = equip_str[:-2]

        response += "*Step " + str(i+1) + "*:\n" +\
          "Equipment Required: " + equip_str + "\n" +\
          r_step['step'] + "\n\n"
    else:
      response += "_No instructions available for this recipe._\n\n"

    response += "*Shoot at my anything else...*"
    return response


def search_food(intent_request):
    output_session_attributes = intent_request['sessionAttributes']
    #get slots from the intent
    source = intent_request['invocationSource']
    slots = get_slots(intent_request)
    validation_result = False
    if source == 'FulfillmentCodeHook':
        #TODO basic validation on input slot
    results = intent_request['inputTranscript']
    if slots['cuisines']:
        search_term = slots['cuisines']
        if slots['cookTime']:
            search_term += ' under '+ parse_time(slots['cookTime'])
        results = rc.findByCuisine(search_term)
    elif slots['foods']:
        search_term = slots['foods']
        if slots['cookTime']:
            search_term += ' under '+ parse_time(slots['cookTime'])
        results = rc.simpleSearch(search_term)
    response = "Lets see here...\n" + \
        "This is one of my favorites \n"
    for i, recipe in enumerate(results):
        id = recipe['id']
        response += str(i+1) + ". " + recipe['title'] + "\n"
    
    response += make_steps(rc.info(id), rc.steps(id))
    #response += "\nPlease enter the corresponding number of your choice."
    return close(
    output_session_attributes,
    'Fulfilled',
    {
        'contentType': 'PlainText',
        'content': response
    }
    )


