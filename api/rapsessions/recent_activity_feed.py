__author__ = 'MichaelParis'

from feedly.feeds.redis import RedisFeed

class RecentActivityFeed(RedisFeed):
    '''
    Holds the most current activities that are relevant to a user.
    This includes items such as new followers, new raps posted, comments on one
    of my raps, a rapback to one of my raps.
    '''
    key_format = 'activites:normal:%(user_id)s'

    def get_ids(self):
        ids = []
        for elem in self[:]:
            ids.append(elem.object_id)
        return ids

class UserRecentActivityFeed(RecentActivityFeed):

    key_format = 'activities:user:%(user_id)s'