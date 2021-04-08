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
    path('search/', Search.as_view(), name='search'),
    path('u/<slug:username>/', ProfileDetailView.as_view(), name='profile'),
    path('category/', AllCategory.as_view(), name='all'),
    path('category/<slug:category>/<slug:subcategory>/',
         CategoryListView.as_view(), name='subcategory'),
    path('category/<slug:subcategory>/',
         CategoryListView.as_view(), name='category'),

    path('u/<str:owner>/item/<int:pk>/', ItemDetailView.as_view(), name='item_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
