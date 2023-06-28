from django.urls import path
from .views import *
urlpatterns = [
    path('get-post-update-delete-user/', UserListPostUpdateDeleteView.as_view(), name='get-post-update-delete-user'),
    path('get-post-post/', PostListPostView.as_view(), name='get-post-post'),
    path('post/<int:post_id>/', PostGetUpdateDeleteView.as_view(), name='get-update-delete-post'),
    path('get-post-like/', LikeListPostView.as_view(), name='get-post-like'),
    path('like/<int:like_id>/', LikeGetUpdateDeleteView.as_view(), name='get-update-delete-like'),
    
]
