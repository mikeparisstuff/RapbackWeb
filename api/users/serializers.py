from rest_framework import serializers

from api.users.models import Profile


class FlatProfileSerializer(serializers.ModelSerializer):

    def get_profile_picture_url(self, profile):
        if profile.profile_picture:
            return profile.profile_picture.url if profile.profile_picture.url else None
        return None

    profile_picture = serializers.SerializerMethodField('get_profile_picture_url')

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_picture',
            'date_joined',
            'last_login'
        )


class ProfileSerializer(serializers.ModelSerializer):

    def get_num_likes(self, profile):
        if profile:
            return profile.get_num_likes()
        return None

    def get_num_raps(self, profile):
        if profile:
            return profile.get_num_raps()

    def get_profile_picture_url(self, profile):
        if profile.profile_picture:
            return profile.profile_picture.url if profile.profile_picture.url else None
        return None

    def get_followers(self, profile):
        return FlatProfileSerializer(profile.get_followers(), many=True).data

    def get_following(self, profile):
        return FlatProfileSerializer(profile.get_followers(), many=True).data

    # user = UserSerializer()
    following = serializers.SerializerMethodField('get_following')
    followers = serializers.SerializerMethodField('get_followers')

    num_likes = serializers.SerializerMethodField('get_num_likes')
    num_raps = serializers.SerializerMethodField('get_num_raps')
    profile_picture = serializers.SerializerMethodField('get_profile_picture_url')

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_picture',
            'date_joined',
            'last_login',
            'phone_number',
            'num_likes',
            'num_friends',
            'num_raps'
        )