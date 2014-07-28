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
        followers = profile.get_followers()
        if len(followers):
            item = followers[0]
            followers = [follow.user for follow in followers]
            return FlatProfileSerializer(followers, many=True).data
        else:
            return None


    def get_following(self, profile):
        following = profile.get_following()
        if len(following):
            print following
            following = [follow.target for follow in following]
            return FlatProfileSerializer(following, many=True).data
        else:
            return None

    # user = UserSerializer()
    followers = serializers.SerializerMethodField('get_followers')
    following = serializers.SerializerMethodField('get_following')

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
            'num_raps',
            'following',
            'followers'
        )