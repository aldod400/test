"""
URL configuration for TestAPI project.

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
# from utils.general_response import handler404 as custom_handler404, handler500 as custom_handler500
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/product/', include('product.urls')),
    path('api/', include('account.urls')),
    # path('api/token', TokenObtainPairView.as_view()),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# handler404 = custom_handler404
# handler500 = custom_handler500