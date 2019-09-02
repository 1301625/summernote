from django.urls import path,include
from .views import PostListView, PostCreateView ,post_detail, apply_post, apply_list,apply_cancel

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>', post_detail, name='detail'),
    path('new/', PostCreateView.as_view(), name='new'),
    path('<int:pk>/apply', apply_post, name='apply'),
    path('<int:pk>/apply_list',apply_list, name='apply_list'),
    path('<int:pk>/apply_cancel', apply_cancel, name='apply_cancel'),
]