#/usr/bin/env python
import requests

def gsearch(phenny, input):
    term = input.group(2)
    if not term:
        return phenny.reply('I need a search term.')
    request = requests.get('http://www.google.com/search?q='+term+'&btnI')
    phenny.say(request.url)

gsearch.commands = ['g', 'google']
gsearch.priority = 'high'
