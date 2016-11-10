#!/usr/bin/env python
"""
backlog-tldr.py - Backlog summarization features

Dependencies
For Summa:
`pip install numpy scipy networkx summa`
For Sumy:
`pip install sumy nltk numpy`
`python -c "import nltk; nltk.download('punkt')"`
"""

# Summa (Currently only works with python2.7)
from sys import modules
try:
    import summa
except ImportError:
    pass

# Sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer

# Import all summarizers until a good working one is chosen
AVAILABLE_METHODS = {
    "luhn": LuhnSummarizer,
    "edmundson": EdmundsonSummarizer,
    "lsa": LsaSummarizer,
    "text-rank": TextRankSummarizer,
    "lex-rank": LexRankSummarizer,
    "sum-basic": SumBasicSummarizer,
    "kl": KLSummarizer,
}

# Config
LANGUAGE = "german"

def setup(self):
    pass


# Summa
def backlog_summa(jenni, input):
    """Parses the backlog of the current channel and creates a summary with summa"""
    backlog_length = 500
    summary_length = 8

    # Use sumy if summa is not available
    try:
        module = modules["summa"]
    except KeyError:
        backlog_sumy(jenni, input)
        return

    channel = input.sender
    nick = input.nick
    command = input.group(1)
    cmds = input.group().split()
    if len(cmds) > 1 and cmds[1].isdigit():
        backlog_length = int(cmds[1])
    if len(cmds) > 2 and cmds[2].isdigit():
        summary_length = int(cmds[2])

    # Backlog is only logged for channels
    if not channel.startswith("#"):
        return

    backlog = jenni.backlog(jenni, channel, backlog_length)
    backlog_str = "\n".join(backlog)

    # Get summary
    if command != "keywords":
        summary = summa.summarizer.summarize(backlog_str, language=LANGUAGE, words=summary_length*10)
        jenni.say("Summary:")
        for line in summary.split("\n"):
            jenni.say(line)

    # Get keywords
    if command != "summary":
        keywords = summa.keywords.keywords(backlog_str, language=LANGUAGE, words=summary_length)
        keyword_str = ", ".join(keywords.split("\n"))
        jenni.say("Keywords: " + str(keyword_str))

backlog_summa.commands = ["summa", "tldr", "summary", "keywords"]
backlog_summa.example = ".summa [backlog_length] [summary_length]"
backlog_summa.priority = "high"


# Sumy
def backlog_sumy(jenni, input):
    """Parses the backlog of the current channel and creates a summary with sumy"""
    backlog_length = 500
    summary_length = 8
    summarize_type = "sum-basic"

    channel = input.sender
    nick = input.nick
    cmds = input.group().split()
    if len(cmds) > 1 and cmds[1].isdigit():
        backlog_length = int(cmds[1])
    if len(cmds) > 2 and cmds[2].isdigit():
        summary_length = int(cmds[2])
    if len(cmds) > 3:
        summarize_type = cmds[3]

    # Backlog is only logged for channels
    if not channel.startswith("#"):
        return

    backlog = jenni.backlog(jenni, channel, backlog_length)
    backlog_str = "\n".join(backlog)

    # Get summary
    parser = PlaintextParser.from_string(backlog_str, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    # Allow selection of summarizer
    summarizer_class = next(cls for name, cls in AVAILABLE_METHODS.items() if summarize_type)
    summarizer = summarizer_class(stemmer)
    if summarizer_class is EdmundsonSummarizer:
        summarizer.null_words = get_stop_words(LANGUAGE)
    else:
        summarizer.stop_words = get_stop_words(LANGUAGE)

    jenni.say("Summary ({}):".format(summarize_type))
    for sentence in summarizer(parser.document, summary_length):
        jenni.say(str(sentence))

backlog_sumy.commands = ["sumy"]
backlog_sumy.example = ".sumy [backlog_length] [summary_length] [luhn,edmundson,lsa,text-rank,lex-rank,sum-basic,kl]"
backlog_sumy.priority = "high"
