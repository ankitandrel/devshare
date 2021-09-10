from django.contrib import admin
from . models import *
# Register your models here.

class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"resource_slug":('resource_name',)}
    list_display = ('resource_name','resource_category','on_homepage', 'is_featured','is_paid')
    list_editable = ('on_homepage','is_featured','is_paid')
    list_display_links = ('resource_name','resource_category',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_name_slug":('category_name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Like_Unlike)
admin.site.register(Article)