__author__ = 'MichaelParis'

from feedly.verbs import register
from feedly.verbs.base import Verb

class Session(Verb):
    id = 1
    infinitive = "rap"
    past_tense = 'rapped'

register(Session)