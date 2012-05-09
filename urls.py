from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings

urlpatterns = patterns('',
    url(r'^$', 'common.views.base'),
    url(r'^user/login/', 'account.views.login'),
    url(r'^logout/?$',  'django.contrib.auth.views.logout_then_login'),
    url(r'^user/register/$',  'account.views.register'),
    url(r'^battle/$',  'battle.views.result'),
    url(r'^battle/send-invitation/$',  'battle.views.send_invitation'),
    url(r'^battle/get-details/$',  'battle.views.get_details'),
    url(r'^battle/disconnect/$',  'battle.views.disconnect'),
    url(r'^battle/attack/$',  'battle.views.attack'),
    url(r'^lobby/join/$',  'lobby.views.join_lobby'),
    url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^plane/create_positioning/(?P<type>.*)/$', 'plane.views.position_coordinates'),
    url(r'^facebook/login$', 'facebook.views.login'),
    url(r'^facebook/authentication_callback$', 'facebook.views.authentication_callback'),
    url(r'^profile/(?P<profile_id>.*)/$', 'account.views.profile'),
    url(r'^alliance/create/$',  'alliance.views.create'),
    url(r'^clan$',  'alliance.views.my_clan'),
    url(r'^clan/avatar$',  'alliance.views.upload_avatar'),
    url(r'^clan/del-member$',  'alliance.views.del_member'),
    url(r'^clan/create-news$',  'alliance.views.create_news'),
    url(r'^clan/name-change$',  'alliance.views.name_change'),
    url(r'^clan/vote-news$',  'alliance.views.vote_news'),
    url(r'^clan/check-like-state$',  'alliance.views.check_like_state'),
    url(r'^alliance/request/$',  'alliance.views.request'),
    url(r'^alliance/process_request/$',  'alliance.views.process_request'),
)