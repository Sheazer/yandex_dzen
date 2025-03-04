from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainView, register, PostView, MarkAddView, CommentListCreateView, \
    AccountView, CommentEditView

urlpatterns = [
    path("login/", CustomTokenObtainView.as_view(), name="login"),
    path('account_register/', register, name='register'),
    path('account/', AccountView.as_view(), name='accounts'),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('post/', PostView.as_view(), name='post-list-create'),
    path('post/<int:pk>/', PostView.as_view(), name='post-retrieve-update-destroy'),
    path('post_add/', PostView.as_view(), name='post-retrieve-update-destroy'),
    path('post/<int:post_id>/mark_add/', MarkAddView.as_view(), name='mark_add'),
    path('post/<int:post_id>/comment/', CommentListCreateView.as_view(), name='comment-list'),
    path('post/<int:post_id>/comment_add/', CommentListCreateView.as_view(), name='comment-create'),
    path('post/<int:post_id>/comment_edit/<int:pk>/', CommentEditView.as_view(), name='comment-detail'),

]
