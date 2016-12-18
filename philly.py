#!/usr/bin/env python3
"""
jenni - An IRC Bot
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/

Note: DO NOT EDIT THIS FILE.
Run ./jenni, then edit ~/.jenni/default.py
Then run ./jenni again
"""

import sys, os, imp, optparse
from configs import Configs
from textwrap import dedent as trim

dotdir = os.path.expanduser('~/.jenni')
configpath = os.path.expanduser(dotdir + '/default.py')

if getattr(os, 'geteuid', None) and os.geteuid() == 0:
    error = 'Error: Refusing to run as root.'
    print(error, file=sys.stderr)
    sys.exit(1)

def check_python_version():
    if sys.version_info < (2, 4):
        error = 'Error: Requires Python 2.4 or later, from www.python.org'
        print(error, file=sys.stderr)
        sys.exit(1)

def create_default_config(fn):
    f = open(fn, 'w')
    output = """\
    # Lines that begin with a "#" are comments.
    # Remove the "#" from the beginning of a line to make those lines active.

    nick = 'jenni'
    host = 'irc.example.net'
    port = 6667
    ssl  = False
    sasl = False
    channels = ['#example', '#test']

    # Channel jenni will report all private messages sent to her to.
    # This includes server notices.
    # logchan_pm = '#jenni-log'

    # You can also specify nick@hostmask
    # For example: yano@unaffiliated/yano
    owner = 'yournickname'

    # user is the NickServ userid
    # This is useful if your NickServ user is different than the nick you are using
    # user = 'userid'

    # password is the NickServ password, serverpass is the server password
    # password = 'example'
    # serverpass = 'serverpass'


    ## API KEYS

    # forecastio_apikey is for an API key from https://forecast.io/
    # This is useful if you want extended weather information.
    # Required if you want .weather to work.
    # If not, you can use .weather-noaa or .wx-noaa
    # forecastio_apikey = ''

    # wunderground_apikey is for an API key from http://www.wunderground.com/
    # This is useful if you want more local and *live* weather information.
    # This is optional and doesn't need to be added.
    # wunderground_apikey = ''

    # google_dev_apikey is for an API key from Google Developers
    # https://developers.google.com/api-client-library/python/guide/aaa_apikeys
    # Get a Server API Key; this is required for YouTube to work.
    # google_dev_apikey = ''

    # wolframalpha_apikey is for an API key from Wolfram|Alpha
    # http://products.wolframalpha.com/api/
    # This is needed in order to make .calc/.c have more comprehensive answers.
    # wolframalpha_apikey = ''


    # twitter_consumer_key and twitter_consumer_secret are for Twitter's API
    # https://apps.twitter.com/
    # This is needed if you'd like to make .twitter usable
    # twitter_consumer_key = ''
    # twitter_consumer_secret = ''

    # Fill in Yelp API information here
    # This is for using the .food command
    yelp_api_credentials = {
        'consumer_key': '',
        'consumer_secret': '',
        'token': '',
        'token_secret': ''
        }

    # api.ai https://docs.api.ai/docs/get-started

    # apiai_apikey = ''

    # google custom search
    # https://developers.google.com/custom-search/
    # http://stackoverflow.com/a/5615931

    # cse_apikey = ''
    # cse_appid = ''


    # openweathermap
    # owm_apikey = ''

    # You can add bannable words / regex per channel
    # bad_words = {
    #   "#yourchan": ['badword', '(a|b).*c.*(d|e)']
    # }
    #
    # This controls the number of warnings a user will receive
    # before they are banned from the channel
    # bad_word_limit = 1

    # auto_title_disable_chans is for disabling the auto URL title feature
    # simply add a channel to this list (preferably in all lower-case)
    # and it won't auto-title URLs in that channel, but .title and other features
    # will still work
    # auto_title_disable_chans = ['##yano',]

    # These are people who will be able to use admin.py's functions...
    admins = [owner, 'someoneyoutrust']
    # But admin.py is disabled by default, as follows:
    exclude = ['adminchannel', 'chicken_reply', 'insult', 'lispy', 'twss']

    # This allows one to allow specific people to use ".msg channel message here"
    # in specific channels.
    helpers = {
        '#channel1': ['a.somedomain.tld', 'b.anotherdomain.tld'],
        '##channel2': ['some/other/hostmask'],
        }

    # Enable raw logging of everything jenni sees.
    # logged to the folder 'log'
    logging = False

    # Block modules from specific channels
    # To not block anything for a channel, just don't mention it
    excludes = {
            '##blacklist': ['!'],
        }

    # If you want to enumerate a list of modules rather than disabling
    # some, use "enable = ['example']", which takes precedent over exclude
    #
    # enable = []

    # Directories to load user modules from
    # e.g. /path/to/my/modules
    extra = ['""" + os.getcwd() + '/modules/' + """']

    # Services to load: maps channel names to white or black lists
    external = {
        '#liberal': ['!'], # allow all
        '#conservative': [], # allow none
        '*': ['!'] # default whitelist, allow all
    }

    # insult database available: "spanish" and "english"
    insult_lang = "english"

    # EOF
    """
    print(trim(output), file=f)
    f.close()

def create_configfile(dotdir):
    if not os.path.isdir(dotdir):
        print('Creating a config directory at ~/.jenni...')
        try: os.mkdir(dotdir)
        except Exception as e:
            print('There was a problem creating %s:' % dotdir, file=sys.stderr)
            print(e.__class__, str(e), file=sys.stderr)
            print('Please fix this and then run jenni again.', file=sys.stderr)
            sys.exit(1)

    create_default_config(configpath)
    print('Config file generated. Please edit it at ' + configpath + ' and run ./jenni again.', file=sys.stdout)

    sys.exit(0)

def check_dotdir():
    if not os.path.isdir(dotdir) or not os.path.isfile(configpath):
        create_configfile(dotdir)

def config_names(config):
    config = config or 'default'

    def files(d):
        names = os.listdir(d)
        return list(os.path.join(d, fn) for fn in names if fn.endswith('.py'))

    here = os.path.join('.', config)
    if os.path.isfile(here):
        return [here]
    if os.path.isfile(here + '.py'):
        return [here + '.py']
    if os.path.isdir(here):
        here_files = files(here)
        if(len(here_files) == 0):
            print("Error: Config directory '{0}' contained no .py files".format(here), file=sys.stderr)
        return here_files

    there = os.path.join(dotdir, config)
    if os.path.isfile(there):
        return [there]
    if os.path.isfile(there + '.py'):
        return [there + '.py']
    if os.path.isdir(there):
        there_files = files(there)
        if(len(there_files) == 0):
            print("Error: Config directory '{0}' contained no .py files".format(there), file=sys.stderr)
        return there_files

    print("Error: Couldn't find config '{0}' to import or .py files therein".format(config), file=sys.stderr)
    sys.exit(1)

def initialize_configs(config_path):
    config_modules = []

    all_configs = config_names(config_path)

    if(len(all_configs) == 0):
        print("Error: no config files found in config path '{0}'".format(config_path), file=sys.stderr)
        sys.exit(1)

    config_helper = Configs(all_configs)
    config_helper.load_modules(config_modules)

    # Give at least one module the config helper
    config_modules[0].config_helper = config_helper

    # Step Four: Load jenni

    try: from __init__ import run
    except ImportError:
        try: from jenni import run
        except ImportError:
            print("Error: Couldn't find jenni to import", file=sys.stderr)
            sys.exit(1)

    # Step Five: Initialise And Run The jennies

    # @@ ignore SIGHUP
    for config_module in config_modules:
        run(config_module) # @@ thread this

def main(argv=None):
    # Step One: Parse The Command Line

    parser = optparse.OptionParser('%prog [options]')
    parser.add_option('-c', '--config', metavar='fn',
        help='use this configuration file or directory')
    opts, args = parser.parse_args(argv)

    # Step Two: Check Dependencies

    check_python_version() # require python2.4 or later
    check_dotdir() # require ~/.jenni, or make it and exit

    # Step Three: Load The Configurations

    initialize_configs(opts.config)

if __name__ == '__main__':
    main()
