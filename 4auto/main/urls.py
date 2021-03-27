"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from webapp.views import *
from django.urls import reverse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    path('', IndexView.as_view(), name='index'),
    path('u/<slug:username>/', ProfileDetailView.as_view(), name='profile'),
    path('category/', AllCategory.as_view(), name='all'),
    path('category/<slug:category>/<slug:subcategory>/',
         CategoryListView.as_view(), name='subcategory'),
    path('category/<slug:subcategory>/',
         CategoryListView.as_view(), name='category'),

    path('u/<str:owner>/item/<int:pk>/', ItemDetailView.as_view(), name='item_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
