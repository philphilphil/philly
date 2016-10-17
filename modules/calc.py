import urllib.parse
import urllib.request

def c(phenny, input):
    calc = input.group(2)
    try:
        req = urllib.request.urlopen('https://www.calcatraz.com/calculator/api?c='+urllib.parse.quote_plus(calc), timeout=2)
        result = req.read().decode('utf-8').strip()
        return phenny.say(result)
    except urllib.error.HTTPError as error:
        return phenny.say(error.code)

c.commands = ['c', 'calc']
