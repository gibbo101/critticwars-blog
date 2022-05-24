from . import views
from django.urls import path


urlpatterns = [
    path('', views.BlogList.as_view(), name='home'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name='blog'),
    path('like/<slug:slug>', views.BlogLike.as_view(), name='blog_like'),
]
