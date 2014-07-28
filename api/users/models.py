
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        return self.clip_set.all().count()

    def get_num_likes(self):
        return self.like_set.all().count()

    def get_likes(self):
        return self.like_set.all().order_by('-created')

    def get_liked_sessions(self):
        likes = self.like_set.all()
        print 'Get liked sessions'
        sessions = [like.session for like in likes];
        return sessions

    def __unicode__(self):
        return 'Profile {}: {}'.format(self.pk, self.username)

class Follow(models.Model):
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
