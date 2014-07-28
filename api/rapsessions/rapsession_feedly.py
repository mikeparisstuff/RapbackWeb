__author__ = 'MichaelParis'

from feedly.feed_managers.base import Feedly, FanoutPriority

from .rapsession_feed import SessionFeed, UserSessionFeed
from api.users.models import Follow

class SessionFeedly(Feedly):

    feed_classes = dict(
        normal = SessionFeed
    )

    user_feed_class = UserSessionFeed

    def add_session(self, session):
        activity = session.create_activity()
        self.add_user_activity(session.creator.id, activity)

    def remove_session(self, session):
        activity = session.create_activity()
        self.remove_user_activity(session.id, activity)

    def get_user_follower_ids(self, user_id):
        ids = Follow.objects.filter(target=user_id).values_list('user_id', flat=True)
        return {FanoutPriority.HIGH:ids}

feedly = SessionFeedly()