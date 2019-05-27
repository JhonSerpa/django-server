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

urlpatterns = [
    # web services
    path('ws/allmedia', views.get_all_media),
    path('ws/media', views.get_media),
    path('ws/addmedia', views.add_media),
    path('ws/removemedia/<str:name>', views.del_media),

    path('ws/allmediaauthors', views.get_all_media_authors),
    path('ws/mediaauthors', views.get_media_authors),
    path('ws/addmediaauthors', views.add_media_author),
    path('ws/removemediaauthors/<int:id>', views.get_all_media),

    path('ws/allreviews', views.get_all_media),
    path('ws/reviewmedia', views.get_all_media),
    path('ws/addreview/<int:id>', views.get_all_media),

    path('ws/user/<int:id>', views.get_all_media),
    path('ws/adduser', views.get_all_media),

    path('', views.home, name='home'),
    path('admin/', admin.site.urls),

]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
