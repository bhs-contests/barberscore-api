from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

from rest_framework import routers

from apps.convention.views import (
    ContestantViewSet,
    PerformanceViewSet,
    ContestViewSet,
)


router = routers.DefaultRouter()
router.register(r'contestant', ContestantViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'contest', ContestViewSet)

urlpatterns = patterns(
    '',
    # Website
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt'), name='robots'),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml'), name='sitemap'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^search/', include('haystack.urls')),
    url(r'', include('apps.convention.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# s
#     # Website
#     url(r'^faq/$', TemplateView.as_view(template_name='website/faq.html'), name='faq'),
#     url(r'^legal/$', TemplateView.as_view(template_name='website/legal.html'), name='legal'),
#     url(r'^support/$', TemplateView.as_view(template_name='website/support.html'), name='support'),
#     url(r'^intro/$', 'intro', name='intro'),
