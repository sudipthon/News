"""
URL configuration for gorkhapatra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import \
    settings
from django.conf.urls.static import \
    static
from django.contrib import \
    admin
from django.urls import (include, path)

urlpatterns = [
    path("hamroadmin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("baseapp.urls")),
]

import logging

logger = logging.getLogger('this is hahaha haha')
logger.info('haha')
logger.debug('haha hahah ahahah')
logger.error('haha')
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.conf import settings
# from django.urls import include, path

# if settings.DEBUG:
#     import debug_toolbar

#     urlpatterns = [
#         path("__debug__/", include(debug_toolbar.urls)),
#         # ... other URL patterns
#     ] + urlpatterns
