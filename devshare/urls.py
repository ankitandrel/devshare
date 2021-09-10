from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('users/', include('users.urls')),
    path('resource/',include('resource.urls')),
    path('form/',include('form.urls')),
    path('view_all_category/',views.view_all_category,name='view_all_category'),
    path('article/',views.article,name='article'),
    path('post_article/',views.post_article,name='post_article'),
    path('article_like/<int:id>/',views.article_like,name='article_like'),
    path('tag/<slug:slug>/', views.article_by_tag, name='article_by_tag'),
    path('search/', views.search,name='search'),
    path('about/', views.about,name='about')
    

]

urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'devshare Administration'
admin.site.index_title = 'devshare Administration'