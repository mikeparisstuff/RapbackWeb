import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.core.verbs import *
# from api.rapsessions.recent_activity_feedly import feedly as recent_activity_feedly
from api.users.models import Profile, Follow
from api.users.serializers import ProfileSerializer, FlatProfileSerializer
from api.core.api import AuthenticatedView, UnauthenticatedView

from stream_django.feed_manager import feed_manager


class WelcomePage(APIView):
    def get(self, request, format=None):
        # increment_page_hit_count.delay()
        return Response('Welcome to the Rapchat API.  Goto /api-docs/ for more details.')

class HandleProfiles(APIView):

    def post(self, request, format=None):
        '''
        Create a new user profile.
        Return the information on the newly created user.

        Returns Appropriately:
        {
            "user": {
                ...
                userinfo
                ...
            },
            "phone_number": "",
            "token": "4a2483f4a94b9ff0447945a9d03ebf048e7faf8d"
        }

        email (required) -- Email address for the new user
        username (required) -- The new user's rapback username
        password (required) -- Password for the new user's account
        first_name (optional) -- Profile's first name
        last_name (optional) -- Profile's last name
        phone_number (optional) -- Profile's current smartphone number
        profile_picture (optional) -- A Square clipped profile picture encoded as jpg
        '''
        try:
            profile = Profile.objects.create_user(
                request.DATA['username'],
                request.DATA['email'],
                request.DATA['password']
            )
            if 'first_name' in request.DATA:
                profile.first_name = request.DATA['first_name']
            if 'last_name' in request.DATA:
                profile.last_name = request.DATA['last_name']

            token = Token.objects.get(user=profile)

            if 'phone_number' in request.DATA:
                profile.phone_number = request.DATA['phone_number']
            if 'profile_picture' in request.FILES:
                f = request.FILES['profile_picture']
                profile.profile_picture = f
            profile.save()
            serializer = ProfileSerializer(profile)
            serializer.data['token'] = token.key
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except KeyError:
            error = {
                'error': "Profile's must have a username, email address, and password"
            }
            return Response(
                error,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, format=None):
        '''
        Return all user profiles
        '''
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HandleProfile(AuthenticatedView):
    def get(self, request, format=None, username=None):
        '''
        Return a profiles designated by the profile id in the url /users/<id>/
        '''
        try:
            profile = Profile.objects.get(username=username)
            prof_serializer = ProfileSerializer(profile)
            likes = profile.get_likes()
            return Response({
                'profile': prof_serializer.data
                }, status=status.HTTP_200_OK
            )
        except Profile.DoesNotExist:
            return Response({
                'error': 'Could not find that user'
                })

class HandleSearch(AuthenticatedView):

    def get(self, request, format=None):
        '''
        Search for rapback users!

        username (required) -- The username query to search for as a query parameter
        '''
        try:
            print 'search'
            print 'Query Params: {}'.format(request.QUERY_PARAMS['username'])
            profiles = Profile.objects.filter(username__icontains = request.QUERY_PARAMS['username'], is_staff=False).exclude(username = request.user.username)
            serializer = ProfileSerializer(profiles, many=True)
            return Response({
                'profiles': serializer.data
                }, status=status.HTTP_200_OK
            )
        except Profile.DoesNotExist:
            return Response({
                'profiles': []
                })

class HandleInvites(UnauthenticatedView):

    def get(self, request, format=None):
        '''
        Hit this endpoint to be redirected to the correct app store to download the app
        '''
        type_of_device = None
        if 'iPhone' in request.META['HTTP_USER_AGENT']:
            type_of_device = 'iPhone'
        elif 'Android' in request.META['HTTP_USER_AGENT']:
            type_of_device = 'Android'
        return Response('You are using an {} device'.format(type_of_device))

class HandleFindInContacts(AuthenticatedView):
    def post(self, request, format=None):
        '''
        Post the list of all the phone-numbers in the contacts.
        Returns all the users that are in the contacts list
        '''
        try:
            numbers = json.loads(request.DATA['phone_numbers'])
            users = Profile.objects.filter(phone_number__in = numbers)
            serializer = FlatProfileSerializer(users, many=True)
            return Response(
                {"users": serializer.data},
                status = status.HTTP_200_OK
            )
        except KeyError:
            return Response(
                {"error": "Must submit a list of phone_numbers to check for contacts"},
                status = status.HTTP_400_BAD_REQUEST
            )

class HandleRecentActivity(AuthenticatedView):
# TODO: NEED TO FIX THIS WITH ENRICHMENT
    def get(self, request, format=None):
        # feed = recent_activity_feedly.get_feeds(request.user.id)['normal']
        # user_feed = recent_activity_feedly.get_user_feed(request.user.id)
        # feed = feed_manager.get_feed(limit=25)['results']
        # activities = feed[:]
        feed = feed_manager.get_feed('notification', request.user.id)
        aggregates = feed.get(limit=25)
        aggregates = aggregates['results']
        # activities.extend(user_feed[:])
        recent_activities = []
        for aggregate in aggregates:
            activities = aggregate['activities']
            for activity in activities:
                actor_id = activity['actor'].split(':')[1]
                object_id = activity['object'].split(':')[1]
                if activity['verb'] == 'like':
                    act = {
                        'type': 'LIKE',
                        'actor_id': actor_id,
                        'object_id': object_id,
                        'time': activity['time'],
                        'extra_context': {
                            'target_username': activity.get('target_username'),
                            'actor_username': activity.get('actor_username'),
                            'actor_profile_picture_url': activity.get('actor_profile_picture_url')
                        }
                    }
                    recent_activities.append(act)
                elif activity['verb'] == 'follow':
                    recent_activities.append({
                        'type': 'FOLLOW',
                        'actor_id': actor_id,
                        'object_id': object_id,
                        'time': activity['time'],
                        'extra_context': {
                            'target_username': activity.get('target_username'),
                            'actor_username': activity.get('actor_username'),
                            'actor_profile_picture_url': activity.get('actor_profile_picture_url')
                        }
                    })
                elif activity['verb'] == 'rapsession':
                    recent_activities.append({
                        'type': 'SESSION',
                        'actor_id': actor_id,
                        'object_id': object_id,
                        'time': activity['time'],
                        'extra_context': {
                            'actor_username': activity.get('actor_username'),
                            'actor_profile_picture_url': activity.get('actor_profile_picture_url')
                        }
                    })
                elif activity['verb'] == 'comment':
                    recent_activities.append({
                        'type': 'COMMENT',
                        'actor_id': actor_id,
                        'object_id': object_id,
                        'time': activity['time'],
                        'extra_context': {
                            'session_id': activity.get('session_id'),
                            'actor_username': activity.get('actor_username'),
                            'actor_profile_picture_url': activity.get('actor_profile_picture_url')
                        }
                    })
        return Response(recent_activities, status=status.HTTP_200_OK)

class HandleMyProfile(AuthenticatedView):

    def get(self, request, format=None):
        '''
        Get my profile.
        '''
        # me = Profile.objects.get(username = request.user.username)
        me = request.user
        serializer = ProfileSerializer(me)
        return Response({
            "profile": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, format=None):
        '''
        Update my profile

        first_name (required) -- The users first name
        last_name (required) -- The users last name
        email (required) -- The users email address
        phone_number (required) -- The users phone number in format 'xxx-xxx-xxxx'
        profile_picture (optional) -- A square clipped jpg to act as the users profile picture
        '''
        print "{0}".format(request.DATA)
        me = request.user
        print 'ME: {0}'.format(me)
        try:
            me.first_name = request.DATA['first_name']
            me.last_name = request.DATA['last_name']
            me.email = request.DATA['email']
            me.phone_number = request.DATA['phone_number']
            if 'profile_picture' in request.FILES:
                f = request.FILES['profile_picture']
                me.profile_picture = f
            me.save()
            print 'updated profile'
            serializer = ProfileSerializer(me)
            return Response({
                'profile': serializer.data
                }, status=status.HTTP_200_OK
            )
        except KeyError as e:
            print e
            return Response({
                'error': 'Must include first_name, last_name, email, and phone_number'
                }, status=status.HTTP_400_BAD_REQUEST
            )

class HandleFollowers(AuthenticatedView):

    def post(self, request, format=None):
        '''
        Create a new Follow relationship.

        target (required) -- The username of the user that you are trying to follow
        '''
        me = request.user

        try:
            target_uname = request.DATA['target']
            target = Profile.objects.get(username=target_uname)
            f, created = Follow.objects.get_or_create(
                user = me,
                target = target
            )

            # recent_activity_feedly.add_recent_activity(f, me.id)
            return Response({
                'detail': 'Successfully followed user with username: {}'.format(target_uname)
                }, status = status.HTTP_201_CREATED
            )
        except KeyError:
            return Response({
                'error': "Must include a 'target' username in order to follow someone"
                }, status = status.HTTP_400_BAD_REQUEST
            )
        except Profile.DoesNotExist:
            return Response({
                'error': "The user you are trying to follow does not exist"
                }, status = status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response({
                'error': e
            }, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        '''
        Unfollow a user with a given username.

        target (required) -- The username of the user that you want to unfollow
        '''
        me = request.user
        try:
            target_uname = request.GET['target']
            target = Profile.objects.get(username=target_uname)
            Follow.objects.get(user = me, target = target).delete()
            feed_manager.unfollow_user(me.id, target.id)
            return Response({
                'detail': 'Successfully unfollowed user with username: {}'.format(target_uname)
                }, status = status.HTTP_200_OK
            )
        except KeyError:
            return Response({
                'error': "Must include a 'target' username in order to unfollow someone"
                }, status = status.HTTP_400_BAD_REQUEST
            )
        except Profile.DoesNotExist:
            return Response({
                'error': "The user you are trying to unfollow does not exist"
                }, status = status.HTTP_400_BAD_REQUEST
            )
        except Follow.DoesNotExist:
            return Response({
                'error': "You are not following the user you are trying to unfollow"
                }, status = status.HTTP_400_BAD_REQUEST
            )