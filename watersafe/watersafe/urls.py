from django.conf.urls import patterns, include, url
from watersafe_site.views import Search, LearnMore, search_form

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    ('^$', search_form),
    ('^results$', Search),
    ('^learn_more$', LearnMore),
    # url(r'^$', 'watersafe.views.home', name='home'),
    # url(r'^watersafe/', include('watersafe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
