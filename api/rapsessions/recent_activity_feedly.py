__author__ = 'MichaelParis'

from feedly.feed_managers.base import Feedly, FanoutPriority

from .recent_activity_feed import RecentActivityFeed, UserRecentActivityFeed
from api.users.models import Follow

class RecentActivityFeedly(Feedly):

    feed_classes = dict(
        normal = RecentActivityFeed
    )

    user_feed_class = UserRecentActivityFeed

    fanout_chunk_size = 1

    def add_recent_activity(self, model, user_id):
        activity = model.create_activity()
        self.add_user_activity(user_id, activity)

    def remove_recent_activity(self, model, user_id):
        activity = model.create_activity()
        self.remove_user_activity(user_id, activity)

    def get_user_follower_ids(self, user_id):
        ids = Follow.objects.filter(target=user_id).values_list('user_id', flat=True)
        return {FanoutPriority.HIGH:ids}

feedly = RecentActivityFeedly()
