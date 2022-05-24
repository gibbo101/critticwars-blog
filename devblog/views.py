from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Blog

class BlogList(generic.ListView):
    model = Blog
    querysey = Blog.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5


class BlogDetail(View):

    def get(self, slug, *args, **kwargs):
        queryset = Blog.objects
        blog = get_object_or_404(queryset, slug=slug)
        comments = blog.comments.order_by('-created_on')
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog.html",
            {
                "blog": blog,
                "comments": comments,
                "liked": liked
            },
        )
