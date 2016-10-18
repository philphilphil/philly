#!/usr/bin/env python
import apiai
import numpy
import json
import re

nowords = ['reload', 'help', 'tell', 'ask', 'ping']

def chat(phenny, input):
    nick = input.group()
    text = input.group(2)

    for x in nowords:
        if text.startswith(x):
            return

    if text.startswith('.'):
        return

    if nick.startswith(phenny.config.nick + ':'):
        if not phenny.config.apiai_apikey:
            return phenny.say('Please set api.ai api key first')

        ai = apiai.ApiAI(phenny.config.apiai_apikey)
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

if __name__ == "__main__":
    print(__doc__.strip())
