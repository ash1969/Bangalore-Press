from django.urls import path
from .views import *

app_name="profile"
urlpatterns = [
    path('post/', new_post, name="new_post"),
    path('edit_post/<int:id>/', edit_post, name='edit_post'),
    path('open_feed/', open_feed, name='open_feed'),
    path('edit_voting/<int:id>/', edit_voting, name='edit_voting')
]