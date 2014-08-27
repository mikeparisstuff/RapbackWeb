from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.users import views as users_views
from api.rapsessions import views as sessions_views
from api.feedback import views as feedback_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rapback.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'api-docs', include('rest_framework_swagger.urls')),

    # USER ENDPOINTS
    url(r'^$', users_views.WelcomePage.as_view(), name='welcome_page'),
    url(r'^users/$', users_views.HandleProfiles.as_view(), name='create_new_user'),
    url(r'^users/(?P<username>\w{3,50})/$', users_views.HandleProfile.as_view(), name='handle_user'),
    url(r'^users/(?P<user_id>\d+)/sessions/$', sessions_views.HandleProfileSessions.as_view(), name='handle_user'),
    url(r'^users/me/$', users_views.HandleMyProfile.as_view(), name='get_my_user'),
    url(r'^users/me/likes/$', sessions_views.HandleRapSessionLikes.as_view(), name='get_my_likes'),
    url(r'^users/me/clips/$', sessions_views.HandleMyRapSessionClips.as_view(), name='get_my_clips'),
    url(r'^users/me/follow/$', users_views.HandleFollowers.as_view(), name='handle_followers'),
    url(r'^users/me/recent/$', users_views.HandleRecentActivity.as_view(), name='handle_recent_activity'),
    url(r'^sessions/rapbacks/(?P<session>\d+)/$', sessions_views.HandleRapbacks.as_view(), name='handle_rapbacks'),
    url(r'^sessions/viewcount/(?P<session>\d+)/$', sessions_views.HandleViewCount.as_view(), name='handle_view_count'),

    url(r'^users/obtain-token/$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^invite/$', users_views.HandleInvites.as_view(), name='invite_users'),
    url(r'^search/$', users_views.HandleSearch.as_view(), name='search_users'),

    url(r'^feedback/$', feedback_views.HandleFeedback.as_view(), name='handle_feedback'),

    # SESSIONS ENDPOINTS
    url(r'^users/me/sessions/$', sessions_views.HandleRapSessions.as_view(), name='handle_sessions'),
    url(r'^users/me/sessions/live/$', sessions_views.HandleRapSessions.as_view(), name='handle_sessions'),
    url(r'^sessions/(?P<session>\d+)/$', sessions_views.HandleRapSession.as_view(), name='handle_single_session'),
    # url(r'^sessions/(?P<session>\d+)/clips/$', sessions_views.HandleRapSessionClips.as_view(), name='handle_clips'),
    url(r'^sessions/(?P<session>\d+)/comments/$', sessions_views.HandleRapSessionComments.as_view(), name='handle_session_comments'),

    url(r'^admin/', include(admin.site.urls)),
)
