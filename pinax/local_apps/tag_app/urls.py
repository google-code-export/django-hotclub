from django.conf.urls.defaults import *

from tag_app import views


urlpatterns = patterns('',
    # all tags
	url(r'^(?P<tag>.+)/$', 'tag_app.views.tags', name='tag_results'),
)
