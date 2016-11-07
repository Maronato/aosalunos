from django.conf import settings
from django.conf.urls import patterns, include, url
from misago.admin import ADMIN_PATH, site

# Your deployment urls configuration
# This configuration already contains Misago urls configuration
# If you want to add 3rd party apps urls to your Misago deployment
# Uncomment bottom lines and use them to register custom url's

urlpatterns = patterns('',
    (r'^', include('app.urls')),
    (r'^forum/', include('misago.urls')),
    (r'^party/', include('party.urls')),
    (r'^dac/', include('dac_handler.urls')),
)

# Include admin patterns
if ADMIN_PATH:
    urlpatterns += patterns('',
        url(r'^' + ADMIN_PATH, include(site.discover())),
    )

# Include admin signout pattern
if ADMIN_PATH:
    urlpatterns += patterns('misago.apps.signin.views',
        url(r'^' + ADMIN_PATH + 'signout/$', 'signout', name="admin_sign_out"),
    )

# Include static and media patterns in DEBUG
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
