__author__ = 'MichaelParis'

from feedly.feeds.redis import RedisFeed

class SessionFeed(RedisFeed):
    '''
    Holds the most current feed for the user with id=user_id taking
    into account all of the people they follow
    '''
    key_format = 'feed:normal:%(user_id)s'

class UserSessionFeed(SessionFeed):
    '''
    A feed that holds of the user with id=user_id most recent posts
    '''
    key_format = 'feed:user:%(user_id)s'