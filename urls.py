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
    url(r'^game/$',  'game.views.initiate_new_game'),
    url(r'^battle/lost_planes_position$',  'battle.views.result'),
    url(r'^battle/send-invitation/$',  'battle.views.send_invitation'),
    url(r'^battle/accept-invitation/$',  'battle.views.accept_invitation'),
    url(r'^battle/get-details/$',  'battle.views.get_details'),
    url(r'^battle/disconnect/$',  'battle.views.disconnect'),
    url(r'^battle/attack/$',  'battle.views.attack'),
    url(r'^lobby/join/$',  'lobby.views.join_lobby'),
    url(r'^hangar/$',  'hangar.views.hangar'),
    url(r'^hangar/equip/$',  'hangar.views.equip'),
    url(r'^hangar/dequip/$',  'hangar.views.dequip'),
    url(r'^hangar/get-wepons/$',  'hangar.views.get_wepons'),
    url(r'^shop/$',  'shop.views.shop'),
    url(r'^shop/items/$',  'shop.views.items'),
    url(r'^shop/buy/$',  'shop.views.buy'),
    url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^plane/create_positioning/(?P<type>.*)/$', 'plane.views.position_coordinates'),
    url(r'^facebook/login$', 'facebook.views.login'),
    url(r'^facebook/authentication_callback$', 'facebook.views.authentication_callback'),
    url(r'^profile/(?P<profile_id>.*)/$', 'account.views.profile'),
    url(r'^404/$', 'common.views.handler404'),
    url(r'^help/$', 'account.views.help'),
)