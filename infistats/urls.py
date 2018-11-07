"""infistats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from image import views
#from imagefit import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^image/', include('image.urls')),
    #url(r'^category/latestImage/', views.CategoryLatest.as_view()),
    # url(r'^category/latestImage/(?P<start_ind>\d+)-(?P<end_ind>\d+)/', views.CategoryLatestWithRange.as_view()),
    url(r'^category/all/', views.AllCategory.as_view()),
    url(r'^tag/all/', views.AllTag.as_view()),

    #url(r'^imagefit/', include('imagefit.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

