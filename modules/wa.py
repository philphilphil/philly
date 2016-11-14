import wolframalpha

def wa(phenny, input):
    if not hasattr(phenny.config, 'wolframalpha_apikey'):
        return phenny.say('Please set Wolfram Alpha AppID.')

    client = wolframalpha.Client(phenny.config.wolframalpha_apikey)

    try:
        request = client.query(input.group(2))
        phenny.say(next(request.results).text)
    except:
        phenny.say('Error')

wa.commands = [ 'wa', 'wolfram', 'wolframalpha' ]
wa.priority = 'high'
