from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Blog
from .forms import CommentForm

class BlogList(generic.ListView):
    model = Blog
    querysey = Blog.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5


class BlogDetail(View):

    def get(self, request, slug, *args, **kwargs):
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
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Blog.objects
        blog = get_object_or_404(queryset, slug=slug)
        comments = blog.comments.order_by('-created_on')
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blog.html",
            {
                "blog": blog,
                "comments": comments,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

class BlogLike(View):

    def blog(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)

        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)

        return HttpResponseRedirect(reverse('blog', args=[slug]))
