"""
webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from app import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    # web services
    path('ws/allmedia', views.get_all_media),
    path('ws/media', views.get_single_media),
    path('ws/addmedia', views.add_media),
    path('ws/removemedia/<str:name>', views.del_media),

    path('ws/allmediaauthors', views.get_all_media_authors),
    path('ws/mediaauthors', views.get_media_authors),
    path('ws/addmediaauthors', views.add_media_author),
    path('ws/removemediaauthors/<int:id>', views.del_media_author),

    path('ws/allreviews', views.get_all_reviews),
    path('ws/mediareviews', views.get_media_reviews),
    path('ws/addreview', views.add_review),
    path('ws/userreviews', views.get_user_reviews),

    path('ws/user', views.get_user),
    path('ws/register', views.register),
    path('ws/login', views.login),
    path('admin/', admin.site.urls),
    path('ws/auth/', ObtainAuthToken.as_view()),
    path('ws/searchmedia', views.search_media),
    path('ws/editauthor', views.edit_author),
    path('ws/editmedia', views.edit_media),
    path('ws/editmediaauthor', views.edit_media_author),
    path('ws/getusername', views.get_user_by_token),
    path('ws/edituser', views.edit_user),

]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
