# django imports
from django.urls import path

# local imorts
from . import views
urlpatterns = [
    
    #home page, news list
    path('',views.index,name="index"),
    #News list by category, page
    path('category/<str:urlName>',views.news_by_category,name="category"),
    #Add news page
    path('write/',views.create_news,name="write_news"),
    #Edit news page
    path('edit/<int:id>',views.edit_news,name="edit_news"),
    #Delete news page
    path('delete/<int:id>',views.delete_news,name="delete_news"),
    #News detail page
    path('news/<int:id>',views.single_news,name="single_news"),

    #Ad list page
    path('ads/',views.list_ads,name="ads"),
    #Add Ad page
    path('create-ad/',views.create_ad,name="create_ad"),
    #edit Ad page
    path('edit-ad/<int:id>',views.edit_ad,name="edit_ad"),
    #delete Ad page
    path('delete-ad/<int:id>',views.delete_ad,name="delete_ad"),



]