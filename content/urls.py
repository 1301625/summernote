from django.urls import path,include
from .views import PostListView, PostCreateView ,post_detail

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>', post_detail, name='detail'),
    path('new/', PostCreateView.as_view(), name='new'),
]