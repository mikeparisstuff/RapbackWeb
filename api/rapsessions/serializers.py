from rest_framework import serializers, pagination

from api.users.serializers import FlatProfileSerializer
from api.rapsessions.models import RapSession, Clip, Comment, Like, Beat


class CommentSerializer(serializers.ModelSerializer):

    commenter = serializers.Field(source='creator.username')

    class Meta:
        model = Comment
        fields = (
            'id',
            'commenter',
            'session',
            'text',
            'created_at',
            'modified_at'
        )

class BeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beat
        fields = (
            'id',
            'title',
            'author',
            'filename',
            'duration',
            'created_at',
            'modified_at'
        )

class RapSessionSerializer(serializers.ModelSerializer):

    # May be a cleaner way to get this relationship
    # TODO: investigate
    def get_comments(self, group_session):
        if group_session:
            return CommentSerializer(group_session.get_comments(), many=True).data
        return None

    def get_likes(self, group_session):
        if group_session:
            return group_session.like_set.all().count()
        return None

    def get_clips(self, group_session):
        if group_session:
            return ClipSerializer(group_session.clip_set.filter(session = group_session), many=True).data
        return None

    def get_most_recent_clip_url(self, group_session):
        if group_session:
            clip = group_session.most_recent_clip()
            if clip:
                return clip.clip.url
            return None
        return None

    def get_most_recent_waveform_url(self, group_session):
        if group_session:
            clip = group_session.most_recent_clip()
            if clip:
                try:
                    return clip.waveform_image.url
                except ValueError:
                    return None
            return None
        return None

    # crowd = CrowdSerializer()
    session_creator = FlatProfileSerializer()
    session_receiver = FlatProfileSerializer()
    beat = BeatSerializer()
    clips = serializers.SerializerMethodField('get_clips')
    comments = serializers.SerializerMethodField('get_comments')
    likes = serializers.SerializerMethodField('get_likes')
    # clip_url = serializers.SerializerMethodField('get_most_recent_clip_url')
    # waveform_url = serializers.SerializerMethodField('get_most_recent_waveform_url')

    class Meta:
        model = RapSession
        fields = (
            'id',
            'title',
            'creator',
            'comments',
            'clips',
            'beat',
            # 'is_battle',
            'likes',
            # 'clip_url',
            # 'waveform_url',
            'created_at',
            'modified_at'
        )

class PaginatedRapSessionSerializer(pagination.PaginationSerializer):
    '''
    Serializes page objects of query sets
    '''
    class Meta:
        object_serializer_class = RapSessionSerializer


class ClipSerializer(serializers.ModelSerializer):

    def get_url(self, clip):
        return clip.clip.url

    def get_waveform_url(self, clip):
        if clip.waveform_image:
            return clip.waveform_image.url if clip.waveform_image.url else None
        return None

    creator = FlatProfileSerializer()
    clip_url = serializers.SerializerMethodField('get_url')
    waveform_url = serializers.SerializerMethodField('get_waveform_url')

    class Meta:
        model = Clip
        fields = (
            'id',
            'clip',
            'creator',
            'waveform_url',
            'clip_url',
            'start_time',
            'end_time',
            'times_played',
            'clip_num',
            'session',
            'created_at',
            'modified_at'
        )

class LikeSerializer(serializers.ModelSerializer):

    user = FlatProfileSerializer()
    session = RapSessionSerializer()
    username = serializers.Field(source='user.username')

    class Meta:
        model = Like
        fields = (
            'id',
            'username',
            'session',
            'created_at',
            'modified_at'
        )