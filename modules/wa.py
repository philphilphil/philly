import wolframalpha

def wa(phenny, input):
    if not hasattr(phenny.config, 'wolframalpha_apikey'):
        return phenny.say('Please set Wolfram Alpha AppID.')

    client = wolframalpha.Client(phenny.config.wolframalpha_apikey)

    # sorry!
    try:
        request = client.query(input.group(2))
        phenny.say(next(request.results).text)
    except AttributeError:
        phenny.say('Error')

wa.commands = [ 'wa', 'wolfram', 'wolframalpha' ]
wa.priority = 'high'
