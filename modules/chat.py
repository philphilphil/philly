#!/usr/bin/env python
import apiai
import numpy
import json
import re

CLIENT_ACCESS_TOKEN = ''

nowords = ['reload', 'help', 'tell', 'ask', 'ping']

def chat(phenny, input):
    text = input.group(2)
    for x in nowords:
        if text.startswith(x):
            return

    if not CLIENT_ACCESS_TOKEN:
        return phenny.say('pleae set the client access token first to use this feature.')

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'
    request.query = text

    response = request.getresponse()
    jsondata = json.loads(response.read().decode())
    status = jsondata['status']['code']

    if status == 200:
        phenny.say(jsondata['result']['fulfillment']['speech'])
    else:
        phenny.say(jsondata['status']['errorDetails'])

chat.rule = r'(?i)($nickname[:,]?\s)?(.*)'
