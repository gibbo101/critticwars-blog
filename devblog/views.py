from django.shortcuts import render
from django.views import generic
from .models import Blog

class BlogList(generic.ListView):
    model = Blog
    querysey = Blog.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5
