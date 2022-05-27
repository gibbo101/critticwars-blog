from django.urls import path
from . import views


urlpatterns = [
    path('', views.BlogList.as_view(), name='home'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name='blog'),
    path('like/<slug:slug>/', views.BlogLike.as_view(), name='blog_like'),
    path('<slug:slug>/edit_comment/<id>/', views.CommentEdit.as_view(), name='edit'),
    path('<slug:slug>/delete_comment/<id>/', views.CommentDelete.as_view(), name='delete'),
]
