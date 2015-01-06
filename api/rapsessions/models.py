from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from datetime import datetime

from api.users.models import Profile
from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager

################################ GROUP SESSIONS ##################################

class Beat(models.Model):
    '''
    Rapback beat model
    '''

    # The title of the beat
    title = models.CharField(
        max_length = 64
    )

    # The author of the beat
    author = models.CharField(
        max_length = 64
    )

    # The file of the song in the phone diremctory
    filename = models.CharField(
        max_length = 64
    )

    # The duration of the song in milliseconds
    duration = models.IntegerField(
        default = 0
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank = True,
        null = True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

AUDIO = 'AUDIO'
VIDEO = 'VIDEO'
TYPE_OPTIONS = (
    (AUDIO, 'Audio'),
    (VIDEO, 'Video'),
)

def get_clip_upload_path(self, filename):
    ext = 'mp4' if self.type == VIDEO else 'mp3'
    return 'sessions/session_{}/clip.{}'.format(self.id, ext)

def get_thumbnail_upload_path(self, filename):
    return 'sessions/session_{}/thumbnail.jpg'.format(self.id)


class RapSession(models.Model, Activity):
    '''
    Rapchat Session Model
    '''

    title = models.CharField(
        max_length=100
    )

    type = models.CharField(
        max_length = 8,
        choices = TYPE_OPTIONS,
        default = AUDIO
    )

    creator = models.ForeignKey(
        Profile,
        # related_name='session_creator_set',
        blank = True,
        null = True,
        default = None
    )

    beat = models.ForeignKey(
        Beat
    )

    duration = models.IntegerField(
        default = 0
    )

    clip = models.FileField(
        upload_to=get_clip_upload_path,
        blank=True,
        null=True
    )

    thumbnail = models.FileField(
        upload_to=get_thumbnail_upload_path,
        blank=True,
        null=True
    )

    # The number of times that this clip has been played
    times_played = models.IntegerField(
        default = 0
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank = True,
        null = True
    )

    # Look for performance hike after adding index here: db_index=True
    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True,
        db_index = True
    )

    # Setup actor reference for stream_django
    @property
    def activity_actor_attr(self):
        return self.creator

    @property
    def activity_object_attr(self):
        return self

    @property
    def extra_activity_data(self):
        url = ''
        if self.creator.profile_picture:
            url = self.creator.profile_picture.url
        return {
            'actor_username': self.creator.username,
            'actor_profile_picture_url': url
        }

    @property
    def activity_author_feed(self):
        return 'rapsessions'

    # Changed to use the stream_django module
    # def create_activity(self):
    #     from feedly.activity import Activity
    #     from api.core.verbs import SessionVerb
    #     activity = Activity(
    #         actor = self.creator.id,
    #         verb = SessionVerb,
    #         object = self.id,
    #         time = datetime.utcnow(),
    #         extra_context=dict(
    #             actor_username=self.creator.username,
    #             actor_profile_picture_url=self.creator.profile_picture.url)
    #     )
    #     return activity

    def __unicode__(self):
        return 'Session: {}'.format(self.title)

    def num_likes(self):
        return self.like_set.count()

    # def num_clips(self):
    #     return self.clip_set.count()

    def get_comments(self):
        return self.comment_set.all().order_by('created_at')

    # def get_clips(self):
    #     return self.clip_set.all().order_by('created_at')

    # def most_recent_clip(self):
    #     try:
    #         return self.clip_set.latest('created_at')
    #     except RapSession.DoesNotExist:
    #         return None


def get_waveform_upload_path(self, filename):
    return 'sessions/session_{}/thumbnail.jpg'.format(self.id)

# class Clip(models.Model):
#     '''
#     Rapchat Music Clip
#     '''
#
#     # duration = models.IntegerField()
#
#     clip_num = models.IntegerField(
#         default = 1
#     )
#
#     creator = models.ForeignKey(
#         Profile
#     )
#
#     session = models.ForeignKey(
#         RapSession
#     )
#
#     duration = models.IntegerField(
#         default = 0
#     )
#
#     # The time in the beat that this clip begins measured in milliseconds
#     start_time = models.IntegerField(
#         default = 0
#     )
#
#     # The time in this beat the the clip ends measured in milliseconds
#     end_time = models.IntegerField(
#         default = 0
#     )
#
#     # The number of times that this clip has been played
#     times_played = models.IntegerField(
#         default = 0
#     )
#
#     def get_url(self, clip):
#         return clip.clip.url
#
#     clip = models.FileField(
#         upload_to=get_clip_upload_path
#     )
#
#     waveform_image = models.FileField(
#         upload_to=get_waveform_upload_path,
#         null = True,
#         blank = True
#     )
#
#     created_at = models.DateTimeField(
#         auto_now_add = True,
#         blank = True,
#         null = True
#     )
#
#     modified_at = models.DateTimeField(
#         auto_now = True,
#         blank = True,
#         null = True
#     )
#
# @receiver(post_save, sender=Clip)
# def update_session_modified_timestamp(sender, instance=None, created=False, **kwargs):
#     if created and instance:
#         print 'Updating modified timestamp on session: {}'.format(instance.session.pk)
#         instance.session.save()



class Comment(models.Model, Activity):
    '''
    Rapchat Comment Model
    '''

    # User who made the comment
    creator = models.ForeignKey(
        Profile
    )

    # RapSession being commented on
    session = models.ForeignKey(
        RapSession
    )

    # Comment text
    text = models.CharField(
        max_length=250,
        default = '',
        null = False,
        blank = False
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank=True,
        null=True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

    @property
    def activity_actor_attr(self):
        return self.creator

    @property
    def activity_object_attr(self):
        return self

    # Only notify the person whose rap we are commenting on
    @property
    def activity_notify(self):
        target_feed = feed_manager.get_notification_feed(self.session.creator.id)
        return [target_feed]

    @property
    def extra_activity_data(self):
        url = ''
        if self.creator.profile_picture:
            url = self.creator.profile_picture.url
        return {
            'session_id': self.session.id,
            'actor_username': self.creator.username,
            'actor_profile_picture_url': url
        }

    # def create_activity(self):
    #     from feedly.activity import Activity
    #     from api.core.verbs import CommentVerb
    #     activity = Activity(
    #         actor = self.creator.id,
    #         verb = CommentVerb,
    #         object = self.id,
    #         time = datetime.utcnow(),
    #         extra_context=dict(
    #             session_id=self.session.id,
    #             actor_username=self.creator.username,
    #             actor_profile_picture_url=self.creator.profile_picture.url
    #         )
    #     )
    #     return activity

class Like(models.Model, Activity):
    '''
    Rapchat Like Model
    '''

    # User who made the like
    user = models.ForeignKey(
        Profile
    )

    session = models.ForeignKey(
        RapSession
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank=True,
        null=True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

    # Only notify the person whose rap we are liking
    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_notify(self):
        target_feed = feed_manager.get_notification_feed(self.session.creator.id)
        user_feed = feed_manager.get_notification_feed(self.user.id)
        return [target_feed, user_feed]

    @property
    def extra_activity_data(self):
        url = ''
        if self.user.profile_picture:
            url = self.user.profile_picture.url
        return {
            'session_id': self.session.id,
            'actor_username': self.user.username,
            'actor_profile_picture_url': url
        }

    # def create_activity(self):
    #     from feedly.activity import Activity
    #     from api.core.verbs import LikeVerb
    #     activity = Activity(
    #         actor = self.user.id,
    #         verb = LikeVerb,
    #         object = self.id,
    #         time = datetime.utcnow(),
    #         extra_context=dict(
    #             session_id=self.session.id,
    #             actor_username=self.user.username,
    #             actor_profile_picture_url = self.user.profile_picture.url)
    #     )
    #     return activity


    def __unicode__(self):
        return 'Like: {}'.format(self.session.title)

class Rapback(models.Model):
    '''
    Rapback model. This keeps track of which sessions were recorded in response to
    another session.
    '''
    original = models.ForeignKey(
        RapSession,
        related_name='original_set'
    )

    response = models.ForeignKey(
        RapSession,
        related_name='response_set'
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        blank = True,
        null = True
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )