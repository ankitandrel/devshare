from django.urls import path
from . import views
urlpatterns = [
    path('',views.resource_by_category, name="all_resource"),
    path('<slug:category_name_slug>/',views.resource_by_category, name='resource_by_category'),
    path('resource-like/<int:id>/',views.resource_like,name='resource_like'),
    path('delete_resource/<int:id>/', views.delete_resource, name='delete_resource'),
    path('delete_article/<int:id>/', views.delete_article, name='delete_article')
    
]
