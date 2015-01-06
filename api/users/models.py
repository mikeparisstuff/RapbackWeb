from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager

from rest_framework.authtoken.models import Token

def get_profile_picture_upload_path(self, filename):
    return 'profiles/profile_{}/profile_picture.jpg'.format(self.username)

class Profile(AbstractUser):
    '''
    Registered Rapchat User
    '''

    profile_picture = models.FileField(
        upload_to=get_profile_picture_upload_path,
        null = True,
        blank = True
    )

    phone_number = models.CharField(
        max_length = 15
    )

    modified_at = models.DateTimeField(
        auto_now = True,
        blank = True,
        null = True
    )

    def get_followers(self):
        followers = Follow.objects.filter(target = self).select_related('user')
        return followers

    def get_following(self):
        following = Follow.objects.filter(user = self).select_related('target')
        return following

    def get_profile_picture_url(self, profile):
        return profile.profile_picture.url

    def get_token(self):
        return Token.objects.get(user=self)

    def get_num_raps(self):
        return self.rapsession_set.all().count()

    def get_num_likes(self):
        return self.like_set.all().count()

    def get_likes(self):
        return self.like_set.all().order_by('-created_at')

    def get_liked_sessions(self):
        likes = self.like_set.all()
        print 'Get liked sessions'
        sessions = [like.session for like in likes];
        return sessions

    def __unicode__(self):
        return 'Profile {}: {}'.format(self.pk, self.username)

class Follow(models.Model, Activity):
    '''
    The Rapback follower relation.
    If Michael is following Zach then Michael is the user and Zach is the target
    '''

    user = models.ForeignKey(
        Profile,
        related_name="following_set"
    )

    target = models.ForeignKey(
        Profile,
        related_name="follower_set"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Only notify the person that we are following of the new follow relation
    @property
    def activity_notify(self):
        return [feed_manager.get_notification_feed(self.target.id), feed_manager.get_notification_feed(self.user.id)]

    @property
    def activity_object_attr(self):
        return self

    @classmethod
    def activity_related_models(cls):
        return ['user', 'target']

    @property
    def extra_activity_data(self):
        url = ''
        if self.user.profile_picture:
            url = self.user.profile_picture.url
        return {
            'actor_username': self.user.username,
            'actor_profile_picture_url': url,
            'target_username': self.target.username
        }

    # def create_activity(self):
    #     from feedly.activity import Activity
    #     from api.core.verbs import FollowVerb
    #     prof_pic_url = None
    #     if self.user.profile_picture and (self.user.profile_picture, 'url'):
    #         prof_pic_url = self.user.profile_picture.url
    #     activity = Activity(
    #         actor = self.user.id,
    #         verb = FollowVerb,
    #         object = self.id,
    #         time = datetime.utcnow(),
    #         extra_context = dict(
    #             actor_username=self.user.username,
    #             actor_profile_picture_url=prof_pic_url,
    #             target_username=self.target.username
    #         )
    #     )
    #     return activity

def follow_change(sender, instance, created, **kwargs):
    if instance.deleted_at is None:
        feed_manager.follow_user(instance.user_id, instance.target_id)
    else:
        feed_manager.unfollow_user(instance.user_id, instance.target_id)

def follow_feed(sender, instance, created, **kwargs):
    # feed_manager.follow_user(instance.user_id, instance.target_id)
    feed_manager.get_feed('rapsessions', instance.user_id).follow('rapsessions', instance.target_id)


def unfollow_feed(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user_id, instance.target_id)


post_save.connect(follow_feed, sender=Follow)
post_delete.connect(unfollow_feed, sender=Follow)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
