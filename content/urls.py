from django.urls import path,include
from .views import PostListView, PostCreateView ,post_detail, apply_post, apply_list,apply_cancel, PostUpdateView,PostDeleteView, comment_form

from chat.views import Chatroom

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>', post_detail, name='detail'),
    path('new/', PostCreateView.as_view(), name='new'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete',PostDeleteView.as_view(), name='delete'),

    path('<int:pk>/apply', apply_post, name='apply'),
    path('<int:pk>/apply_list',apply_list, name='apply_list'),
    path('<int:pk>/apply_cancel', apply_cancel, name='apply_cancel'),

    #채팅url
    path('<int:pk>/chat', Chatroom, name="chat"),

    path('commentform',  comment_form, name='comment_form')
]