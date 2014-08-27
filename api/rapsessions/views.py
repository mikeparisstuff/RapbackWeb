from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.response import Response

from api.rapsessions.models import RapSession, AUDIO, VIDEO, Comment, Like, Beat, Rapback
from api.rapsessions.serializers import RapSessionSerializer, CommentSerializer, LikeSerializer, PaginatedRapSessionSerializer
from api.users.models import Profile
from .rapsession_feedly import feedly as session_feedly
from .recent_activity_feedly import feedly as recent_activity_feedly
from api.core.api import AuthenticatedView


####################################################################
#					 	GROUP SESSIONS
####################################################################

class HandleRapSessions(AuthenticatedView):

    def post(self, request, format=None):
        '''
        Create a RapSession

        title (required) -- The title for the rap session
        clip (required) -- The rap clip for the rap session (mp3 if type AUDIO, mp4 if type VIDEO)
        duration (required) -- The duration of the song in milliseconds
        beat_id (required) -- The id of the beat associated with this rap
        type (required) -- The type of the clip either AUDIO or VIDEO.
        thumbnail (required) -- Thumbnail image for the video / album art
        rapback_id (optional) -- The id of the RapSession that is being rapbacked to
        '''
        try:
            title = request.DATA['title']
            clip = request.FILES['clip']
            duration = request.DATA['duration']
            creator = request.user
            thumbnail = request.FILES['thumbnail']
            type = request.DATA['type']

            beat = Beat.objects.get(id = request.DATA['beat_id'])
            print "tick"

            # TODO: This takes two calls to the db because otherwise the id is not populated
            # in time for the thumbnail and clip to use it. Should be rethought
            gs = RapSession.objects.create(
                title = title,
                creator = creator,
                beat = beat,
                type = VIDEO if type == VIDEO else AUDIO,
                duration = duration,
            )
            gs.thumbnail = thumbnail
            gs.clip = clip
            gs.save()
            print "Created session"

            # Create the Rapback record if rapback_id is in the request
            if ('rapback_id' in request.DATA):
                try:
                    session = RapSession.objects.get(id=request.DATA['rapback_id'])
                    Rapback.objects.create(
                        original = session,
                        response = gs
                    )
                except RapSession.DoesNotExist:
                    print 'Session being rapbacked to does not exist'

            recent_activity_feedly.add_recent_activity(gs, request.user.id)
            session_feedly.add_session(gs)

            serializer = RapSessionSerializer(gs)
            return Response(
                {"session": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except KeyError as e:
            print e
            return Response(
                {'error': 'New sessions require a title, clip, duration, beat_id, waveform, and visibility'},
                status=status.HTTP_400_BAD_REQUEST
            )


    def get(self, request, format=None):
        '''
        Return a list of sessions for the currently logged in user.

        TODO: Filter the user data that gets send at this endpoint.
        We probably don't want each users friend information to be being sent etc.
        '''
        # sessions = RapSession.objects.order_by('-modified_at')[:16]

        feed = session_feedly.get_feeds(request.user.id)['normal']
        user_feed = session_feedly.get_user_feed(request.user.id)


        print 'GOT FEED WITH COUNT: {}'.format(feed.count())
        session_ids = feed.get_ids()
        user_session_ids = user_feed.get_ids()
        session_ids.extend(user_session_ids)

        sessions = RapSession.objects.filter(id__in = session_ids).order_by('-created_at')

        print "USER: {0}".format(request.user.username)

        paginator = Paginator(sessions, 6)
        page = request.QUERY_PARAMS.get('page')

        try:
            sessions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            sessions = paginator.page(1)
        except EmptyPage:
            # if page is out of range, return last page
            sessions = paginator.page(paginator.num_pages)


        serializer_context = {'request': request}
        serializer = PaginatedRapSessionSerializer(sessions, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HandleProfileSessions(AuthenticatedView):
    def get(self, request, format=None, user_id = None):
        '''
        Get the personal feed of the user with the given username
        user_id (required) -- The username of the feed to get
        '''
        print "In Request " + user_id
        try:
            profile = Profile.objects.get(id = user_id)
            feed = session_feedly.get_user_feed(profile.id)
            session_ids = feed.get_ids()
            sessions = RapSession.objects.filter(id__in = session_ids).order_by('-created_at')
            serializer = RapSessionSerializer(sessions, many=True)
            return Response({
                'sessions': serializer.data
                }, status = status.HTTP_200_OK
            )
        except KeyError:
            return Response({
                'error': 'Must supply a username'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Profile.DoesNotExist:
            return Response({
                'error': 'Could not find that user'
                }, status=status.HTTP_400_BAD_REQUEST
            )

class HandleRapSession(AuthenticatedView):

    def get(self, request, format=None, session=None):
        '''
        Return a single session as designated by the id in the URL
        '''
        try:
            sesh = RapSession.objects.get(pk=session)
            serializer = RapSessionSerializer(sesh)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RapSession.DoesNotExist:
            return Response({
                'error': 'Could not find a session with that id.'
                }, status=status.HTTP_400_BAD_REQUEST
            )

class HandleRapbacks(AuthenticatedView):

    def get(self, request, format=None, session=None):
        try:
            rapbacks = Rapback.objects.filter(original=session)
            sessions = [rb.response for rb in rapbacks]
            serializer = RapSessionSerializer(sessions, many=True)
            return Response({
                'rapbacks': serializer.data
                }, status=status.HTTP_200_OK
            )
        except RapSession.DoesNotExist:
            return Response({
                'error': 'Could not find the session that matches that id'
                }, status=status.HTTP_400_BAD_REQUEST
            )

class HandleViewCount(AuthenticatedView):

    def post(self, request, format=None, session=None):
        try:
            session = RapSession.objects.get(id=session)
            session.times_played += 1
            session.save()
            return Response(
                'detail: Successfully incremented view count',
                status=status.HTTP_200_OK)
        except RapSession.DoesNotExist:
            return Response(
                'error: Error incrementing view count',
                status=status.HTTP_400_BAD_REQUEST)


# class HandleRapSessionClips(AuthenticatedView):
#
#     def post(self, request, format=None, session=None):
#         '''
#         Add a clip to a session.
#
#         clip (required) -- The clip file to add to the session
#         waveform (required)  -- A jpg image file to serve as a waveform for the clip
#         '''
#         try:
#             sesh = RapSession.objects.get(pk=session)
#             user = request.user
#             profile = user
#             # if sesh.is_battle:
#             # 	sesh.toggle_waiting_on(user.username)
#             f =  request.FILES['clip']
#             waveform = None
#             c = Clip(
#                 clip_num = sesh.num_clips()+1,
#                 session = sesh,
#                 creator = profile
#             )
#             c.clip = f
#             if 'waveform' in request.FILES:
#                 waveform = request.FILES['waveform']
#                 c.waveform = waveform
#             print 'Clip Created'
#             c.save()
#             print 'Clip Saved'
#
#             serializer = ClipSerializer(c)
#
#             return Response({
#                 'clip':serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )
#         except KeyError:
#             return Response(
#                 {'error': 'A clip file and session are required to add a clip'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except RapSession.DoesNotExist:
#             return Response(
#                 {'error': 'The session with id {} could not be found'.format(request.DATA['session'])},
#                 status = status.HTTP_404_NOT_FOUND
#             )
#
#     def get(self, request, format=None, session=None):
#         '''
#         Return data on each of the clips for the session specified in the url.
#         '''
#         try:
#             clips = Clip.objects.filter(session=session)
#             serializer = ClipSerializer(clips, many=True)
#             return Response({'clips': serializer.data}, status=status.HTTP_200_OK)
#         except Clip.DoesNotExist:
#             return Response({
#                 'error': 'Could not find any clips for session {}'.format(session)
#                 }, status=status.HTTP_400_BAD_REQUEST
#             )

class HandleMyRapSessionClips(AuthenticatedView):
    def get(self, request, format=None):
        '''
        Get all my clips.
        '''
        clips = request.user.rapsession_set.all().order_by('-created_at')
        serializer = RapSessionSerializer(clips, many=True)
        return Response({'raps': serializer.data}, status=status.HTTP_200_OK)


class HandleRapSessionComments(AuthenticatedView):
    def post(self, request, format=None, session=None):
        '''
        Add a comment to a session.

        text (required) -- The text of the comment itself
        '''
        try:
            sesh = RapSession.objects.get(pk=session)
            comment = Comment.objects.create(
                session=sesh,
                creator=request.user,
                text = request.DATA['text']
            )
            recent_activity_feedly.add_recent_activity(comment, request.user.id)
            serializer = CommentSerializer(comment)
            return Response({
                'comment': serializer.data,
                'detail': 'Successfully added comment to session %d' % sesh.id
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return Response({
                'error': 'Error creating comment. Comments need a session and comment_text.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, format=None, session=None):
        '''
        Get all of a sessions comments.

        session (required) -- The id of the session. This must be included in the url e.g. /sessions/comments/1/
        would refer to the session with id == 1.
        '''
        try:
            sesh = RapSession.objects.get(pk=session)
            comments = sesh.get_comments()
            # s_serializer = RapSessionSerializer(sesh)
            print ' Found comments'
            c_serializer = CommentSerializer(comments, many=True)
            print 'Serialized comments'
            return Response({
                'comments': c_serializer.data,
                'detail': 'Successfully found comments for session %d' % sesh.id
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return Response({
                'error': 'Need a session to find comments for.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except RapSession.DoesNotExist:
            return Response({
                'error': 'Sorry, we could not find that session.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class HandleRapSessionLikes(AuthenticatedView):
    def post(self, request, format=None):
        '''
        Add a like to a session

        session (required) -- The id of the session to add the comment to
        '''
        try:
            session = RapSession.objects.get(id=request.DATA['session'])
            like = Like.objects.get(
                user = request.user,
                session= session
            )
            serializer = LikeSerializer(like)
            recent_activity_feedly.remove_recent_activity(like, like.user.id)
            like.delete()
            return Response({
                'like': serializer.data
                }, status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            session = RapSession.objects.get(id=request.DATA['session'])
            like = Like.objects.create(
                user= request.user,
                session= session
            )
            try:
                recent_activity_feedly.add_recent_activity(like, like.user.id)
            except ValueError as e:
                print 'Error adding activity to recent activity feed: {}'.format(e)
            serializer = LikeSerializer(like)
            return Response({
                'like': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except KeyError:
            return Response({
                'detail': 'Failed to create like'},
                status = status.HTTP_400_BAD_REQUEST
                )

    def get(self, request, format=None):
        '''
        Get all the likes for the currently logged in user
        '''
        likes = request.user.get_likes()
        print likes
        serializer = None
        if len(likes) > 1:
            serializer = LikeSerializer(likes, many=True)
        else:
            serializer = LikeSerializer(likes)
        return Response({
            'likes': serializer.data
            },
            status = status.HTTP_200_OK
        )