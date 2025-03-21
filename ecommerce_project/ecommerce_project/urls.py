"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from ecommerce_app import views
from django.conf import settings  
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.conf.urls.static import static  
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('ecommerce_app.urls', namespace='ecommerce_app')),
      path('', include('userauth.urls', namespace='userauth')),
      path('', include('selleradmin.urls', namespace='selleradmin')),
  

]

urlpatterns += i18n_patterns(
    # your other urls
     
      path('i18n/setlang/', set_language, name='set_language'),
)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)  

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

