from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.response import Response

from api.rapsessions.models import RapSession, Clip, Comment, Like, Beat
from api.rapsessions.serializers import RapSessionSerializer, ClipSerializer, CommentSerializer, LikeSerializer, PaginatedRapSessionSerializer
from .rapsession_feedly import feedly
from api.core.api import AuthenticatedView


####################################################################
#					 	GROUP SESSIONS
####################################################################

class HandleRapSessions(AuthenticatedView):

    def post(self, request, format=None):
        '''
        Create a RapSession

        title (required) -- The title for the rap session
        clip (required) -- The rap clip for the rap session
        duration (required) -- The duration of the song in milliseconds
        waveform (required) -- The image for the waveform of the first clip
        beat_id (required) -- The id of the beat associated with this rap
        '''
        try:
            title = request.DATA['title']
            clip = request.FILES['clip']
            duration = request.DATA['duration']
            creator = request.user

            beat = Beat.objects.get(id = request.DATA['beat_id'])
            print "tick"
            gs = RapSession.objects.create(
                title = title,
                creator = creator,
                beat = beat
            )
            print "created session"
            # Create Clip
            rap = request.FILES['clip']
            clip = Clip(
                clip_num = 1,
                clip = clip,
                creator = creator,
                session = gs,
                start_time = 0,
                end_time = duration
            )
            if 'waveform' in request.FILES:
                waveform = request.FILES['waveform']
                clip.waveform_image = waveform

            clip.save()
            print "Created Clip. Initiating Session Fanout"

            feedly.add_session(gs)

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

        feed = feedly.get_user_feed(request.user.id)

        print 'GOT FEED WITH COUNT: {}'.format(feed.count())
        session_ids = feed.get_ids()

        sessions = RapSession.objects.filter(id__in = session_ids).order_by('-created_at')

        print "USER: {0}".format(request.user.username)

        paginator = Paginator(sessions, 4)
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

class HandleRapSessionClips(AuthenticatedView):

    def post(self, request, format=None, session=None):
        '''
        Add a clip to a session.

        clip (required) -- The clip file to add to the session
        waveform (required)  -- A jpg image file to serve as a waveform for the clip
        '''
        try:
            sesh = RapSession.objects.get(pk=session)
            user = request.user
            profile = user
            # if sesh.is_battle:
            # 	sesh.toggle_waiting_on(user.username)
            f =  request.FILES['clip']
            waveform = None
            c = Clip(
                clip_num = sesh.num_clips()+1,
                session = sesh,
                creator = profile
            )
            c.clip = f
            if 'waveform' in request.FILES:
                waveform = request.FILES['waveform']
                c.waveform = waveform
            print 'Clip Created'
            c.save()
            print 'Clip Saved'

            serializer = ClipSerializer(c)

            return Response({
                'clip':serializer.data
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return Response(
                {'error': 'A clip file and session are required to add a clip'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except RapSession.DoesNotExist:
            return Response(
                {'error': 'The session with id {} could not be found'.format(request.DATA['session'])},
                status = status.HTTP_404_NOT_FOUND
            )

    def get(self, request, format=None, session=None):
        '''
        Return data on each of the clips for the session specified in the url.
        '''
        try:
            clips = Clip.objects.filter(session=session)
            serializer = ClipSerializer(clips, many=True)
            return Response({'clips': serializer.data}, status=status.HTTP_200_OK)
        except Clip.DoesNotExist:
            return Response({
                'error': 'Could not find any clips for session {}'.format(session)
                }, status=status.HTTP_400_BAD_REQUEST
            )

class HandleMyRapSessionClips(AuthenticatedView):
    def get(self, request, format=None):
        '''
        Get all my clips.
        '''
        clips = request.user.clip_set.all().order_by('-created_at')
        serializer = ClipSerializer(clips, many=True)
        return Response({'clips': serializer.data}, status=status.HTTP_200_OK)


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
            like.delete()
            return Response({
                'like': {'detail': 'Successfully deleted like'}
                }, status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            like = Like.objects.create(
                user= request.user,
                session= session
            )
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