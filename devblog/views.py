from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Blog, Comment
from .forms import CommentForm
import datetime

class BlogList(generic.ListView):
    model = Blog
    queryset = Blog.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10


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

    def post(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)

        return HttpResponseRedirect(reverse('blog', args=[slug]))


class CommentEdit(View):

    def get(self, request, id, *args, **kwargs):
        queryset = Comment.objects
        comment = get_object_or_404(queryset, id=id)

        return render(
            request,
            "edit_comment.html",
            {
                "comment": comment,
                "comment_form": CommentForm(instance=comment),
            },
        )

    def post(self, request, slug, id, *args, **kwargs):
        queryset = Comment.objects
        comment = get_object_or_404(queryset, id=id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.updated_on = datetime.datetime.now()
            comment.save()
        else:
            comment_form = CommentForm()

        return HttpResponseRedirect(reverse('blog', args=[slug]))
