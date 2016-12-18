import json
import requests

def weather(phenny, input):
    if not hasattr(phenny.config, 'owm_apikey'):
        return phenny.say('Please set OpenWeatherMap API Key.')

    api = 'http://api.openweathermap.org/data/2.5/weather'
    payload = {'q': input.group(2), 'appid': phenny.config.owm_apikey}

    try:
        req = requests.get(api, params=payload)
        parse = json.loads(req.text)
        temp = parse['main']['temp']
        k2c = temp-273.15
        phenny.say(parse['name'] + ', ' + parse['sys']['country'] + ' - Conditions: ' + parse['weather'][0]['description'] + ', Temperature: ' + str(round(k2c, 2)) +'C')
    except:
        phenny.say('Error')

weather.commands = [ 'weather' ]
weather.priority = 'high'
