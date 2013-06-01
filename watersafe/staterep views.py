from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *

#Uncomment these when you're ready to integrate stuff from Chris's project
#in chris's these were all from StateGovTracker_Django.views import *
#from state_gov_tracker_app.views import home
from state_gov_tracker_app.views import search_form
#from state_gov_tracker_app.views import search_results
from state_gov_tracker_app.views import WhichRep, legislator_list
# from state_gov_tracker_app.views import RecordVote
from state_gov_tracker_app.views import profile, pa_tweets, about_myrep
from blog.views import Blog, Article, BlogPreview
from secretballot.views import vote
from django.contrib import admin
from state_gov_tracker_app.api import PreferencesResource, PR_Resource
from tastypie.api import Api


v1_api = Api(api_name='v1')
v1_api.register(PreferencesResource())
v1_api.register(PR_Resource())

admin.autodiscover()

urlpatterns = patterns('',
    ('^$', search_form),
    ('^results$', WhichRep),
    ('^profile/([A-Z][A-Z]L\d+)/?', profile),
    ('^pa-tweets$', pa_tweets),
    ('^about$', about_myrep),
    url(r'^blog$', Blog),
    url(r'^preview/blog$', BlogPreview),
    url(r'blog/post_num/(.*)$', Article),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
    url(r'^vote/$', vote),
    url(r'^browse_legislators/$', legislator_list),
    # url(r'at_a_glance/$', at_a_glance,)
)