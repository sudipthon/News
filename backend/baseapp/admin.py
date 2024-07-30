from typing import Any
from django.contrib import admin
from django.core.cache import cache


# Register your models here.

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Post,Ad,Category,Tags,Popup

class PostAdmin(admin.ModelAdmin):
        filter_horizontal = ['categories','tags']
        fields = ['headline', 'featured_image','content', 'last_modified', 'categories', 'tags', 'author','status','posted_on','posted_on_bs','views_count']
        readonly_fields = [ 'last_modified','posted_on_bs','author','views_count']
        list_display = ['headline', 'posted_on','last_modified', 'display_categories',  'author',"featured_image",'status','views_count']
        list_filter = ['posted_on','last_modified','categories','author','status']
        search_fields=['headline','author__username','categories__name','tags__name']
        exclude = ['first_paragraph']
        
       

        def save_model(self, request, obj, form, change):
                if not change:  # only set author when the object is first created
                        obj.author = request.user
                super().save_model(request, obj, form, change)
                
        def display_categories(self, obj):
                return ', '.join([category.name for category in obj.categories.all()])
        display_categories.short_description = 'Categories'
        
class CategoryAdmin(admin.ModelAdmin):
        list_display=['name','url_name','display_post_count','display_subcategories']
        list_filter=['name','subcategories']
        def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
                qs= super().get_queryset(request)
                return qs.exclude(name='home')
      
        def display_post_count(self,obj):
                return obj.category_posts.count()
        
        def display_subcategories(self,obj):
                return ', '.join([category.name for category in obj.subcategories.all()])
        
        display_post_count.short_description='Post Count'
        display_subcategories.short_description='Subcategories'
        
class AdAdmin(admin.ModelAdmin):
        list_display=['title','party_name','image','posted_on','expires_on','Ad_Page']
        filter_horizontal = ['categories']
        list_filter=['party_name','categories']
        
        def expires_on(self,obj):
                return obj.expiry_date
        def Ad_Page(self,obj):
                return ', '.join([category.name for category in obj.categories.all()])
        
        
                
admin.site.register(Ad,AdAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tags)
admin.site.register(Post,PostAdmin)
admin.site.register(Popup)