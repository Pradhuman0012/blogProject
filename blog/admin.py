from django.contrib import admin
from blog.models import Post,comment
# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','publish','created','update','status']
    list_filter=('status','author','created','publish')
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=['status','publish']
    prepopulated_fields={'slug':('title',)}

class commentAdmin(admin.ModelAdmin):
    list_display=['post','name','email','body','created','updated','active']
    list_filter=('created','updated','active')
    ordering=['created','updated','active']
    search_fields=['name','email']
admin.site.register(comment,commentAdmin)
admin.site.register(Post,postAdmin)