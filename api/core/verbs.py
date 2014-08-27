__author__ = 'MichaelParis'

from feedly.verbs import register
from feedly.verbs.base import Verb

class SessionVerb(Verb):
    id = 6
    infinitive = "rap"
    past_tense = 'rapped'

class LikeVerb(Verb):
    id = 7
    infinitive = "like"
    past_tense = 'liked'

class FollowVerb(Verb):
    id = 8
    infinitive = 'follow'
    past_tense = 'followed'

class CommentVerb(Verb):
    id = 9
    infinitive = 'comment'
    past_tense = 'commented'

register(SessionVerb)
register(LikeVerb)
register(FollowVerb)
register(CommentVerb)