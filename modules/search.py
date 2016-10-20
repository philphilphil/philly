#/usr/bin/env python
import requests
import json

def gsearch(phenny, input):
    term = input.group(2)
    if not term:
        return phenny.reply('I need a search term.')
    request = requests.get('http://www.google.com/search?q='+term+'&btnI')
    phenny.say(request.url)

gsearch.commands = ['fl', 'fg'] # feeling lucky ; free google
gsearch.priority = 'high'

def gcse(phenny, input):
    if not hasattr(phenny.config, 'cse_apikey'):
        return phenny.say('Please set CSE API Key.')

    if not hasattr(phenny.config, 'cse_appid'):
        return phenny.say('Please set CSE App ID.')

    term = input.group(2)
    if not term:
        return phenny.reply('Please provide a search term.')
    request = requests.get('https://www.googleapis.com/customsearch/v1?key='+phenny.config.cse_apikey+'&cx='+phenny.config.cse_appid+'&q='+term)
    try:
        r = json.loads(request.text)
        return phenny.say(r['items'][0]['link'])
    except KeyError:
        return phenny.say('error')

gcse.commands = [ 'g', 'google' ]
gcse.priority = 'high'
