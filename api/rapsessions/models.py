from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from api.users.models import Profile





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

class RapSession(models.Model):
    '''
    Rapchat Session Model
    '''

    title = models.CharField(
        max_length=100
    )

    # is_complete = models.BooleanField(
    #     default=False
    # )
    #
    # PUBLIC = 'PUBLIC'
    # FRIENDS_ONLY = 'FRIENDS'
    # VISIBILITY_OPTIONS = (
    #     (PUBLIC, 'Public'),
    #     (FRIENDS_ONLY, 'Friends Only'),
    # )

    # visibility = models.CharField(
    #     max_length = 8,
    #     choices = VISIBILITY_OPTIONS,
    #     default = PUBLIC
    # )

    creator = models.ForeignKey(
        Profile,
        related_name='session_creator_set',
        blank = True,
        null = True,
        default = None
    )

    beat = models.ForeignKey(
        Beat
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

    def create_activity(self):
        from feedly.activity import Activity
        from api.core.verbs import Session as SessionVerb
        activity = Activity(
            actor = self.creator.id,
            verb = SessionVerb,
            object = self.id,
            time = datetime.utcnow(),
        )
        return activity

    def __unicode__(self):
        return 'Session: {}'.format(self.title)

    def num_likes(self):
        return self.like_set.count()

    def num_clips(self):
        return self.clip_set.count()

    def get_comments(self):
        return self.comment_set.all().order_by('created_at')

    def get_clips(self):
        return self.clip_set.all().order_by('created_at')

    def most_recent_clip(self):
        try:
            return self.clip_set.latest('created_at')
        except Clip.DoesNotExist:
            return None



def get_clip_upload_path(self, filename):
    return 'sessions/session_{}/clip_{}.mp3'.format(self.session.id, self.clip_num)

def get_waveform_upload_path(self, filename):
    return 'sessions/session_{}/waveform_{}.jpg'.format(self.session.id, self.clip_num)

class Clip(models.Model):
    '''
    Rapchat Music Clip
    '''

    # duration = models.IntegerField()

    clip_num = models.IntegerField(
        default = 1
    )

    creator = models.ForeignKey(
        Profile
    )

    session = models.ForeignKey(
        RapSession
    )

    # The time in the beat that this clip begins measured in milliseconds
    start_time = models.IntegerField(
        default = 0
    )

    # The time in this beat the the clip ends measured in milliseconds
    end_time = models.IntegerField(
        default = 0
    )

    # The number of times that this clip has been played
    times_played = models.IntegerField(
        default = 0
    )

    def get_url(self, clip):
        return clip.clip.url

    clip = models.FileField(
        upload_to=get_clip_upload_path
    )

    waveform_image = models.FileField(
        upload_to=get_waveform_upload_path,
        null = True,
        blank = True
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

@receiver(post_save, sender=Clip)
def update_session_modified_timestamp(sender, instance=None, created=False, **kwargs):
    if created and instance:
        print 'Updating modified timestamp on session: {}'.format(instance.session.pk)
        instance.session.save()



class Comment(models.Model):
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

class Like(models.Model):
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

    def __unicode__(self):
        return 'Like: {}'.format(self.session.title)