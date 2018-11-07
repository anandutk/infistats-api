from django.conf.urls import  url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
urlpatterns = [
    url(r'^all/$', views.AllImages.as_view()),
    url(r'^UpdateFavourite/', views.UpdateFavourite.as_view()),
    url(r'^(?P<start_ind>\d+)-(?P<end_ind>\d+)/$', views.ALlImagesWithRange.as_view()),
    url(r'^countAfterDate/(?P<timeStamp>\d+)/$', views.ImagesCountAfterTime.as_view()),
    url(r'^category/(?P<category>\w+)/$', views.ImagesCategory.as_view()),
    url(r'^category/(?P<category>\w+)/(?P<start_ind>\d+)-(?P<end_ind>\d+)/$', views.ImagesCategoryWithRange.as_view()),
    url(r'^tag/(?P<tag>\w+)/$', views.ImagesTag.as_view()),
    url(r'^tag/(?P<tag>\w+)/(?P<start_ind>\d+)-(?P<end_ind>\d+)/$', views.ImagesTagWithRange.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)