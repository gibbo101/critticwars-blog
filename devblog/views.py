from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Blog, Comment, CwUsers, User
from .forms import CommentForm, CritticWarsForm
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
        num_comments = comments
        cw_users = CwUsers.objects.all()
       
        page = request.GET.get('page', 1)
        paginator = Paginator(comments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog.html",
            {
                "blog": blog,
                "comments": comments,
                "num_comments": num_comments,
                "cw_users": cw_users,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Blog.objects
        users = User.objects
        user = get_object_or_404(users, id=self.request.user.id)
        blog = get_object_or_404(queryset, slug=slug)
        comments = blog.comments.order_by('-created_on')
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment_form.instance.name_id = user
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Added')
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
            comment.updated = True
            comment.save()
        else:
            comment_form = CommentForm()

        return HttpResponseRedirect(reverse('blog', args=[slug]), messages.add_message(request, messages.SUCCESS, 'Comment Edited'))
     
class CommentDelete(View):

    def get(self, request, id, *args, **kwargs):
        queryset = Comment.objects
        comment = get_object_or_404(queryset, id=id)

        return render(
            request,
            "delete_comment.html",
            {
                "comment": comment,
            },
        )

    def post(self, request, slug, id, *args, **kwargs):
        queryset = Comment.objects
        comment = get_object_or_404(queryset, id=id)

        if comment:
            comment.delete()
            return HttpResponseRedirect(reverse('blog', args=[slug]), messages.add_message(request, messages.ERROR, 'Comment Deleted'))
        else:
            return HttpResponseRedirect(reverse('blog', args=[slug]), messages.add_message(request, messages.ERROR, 'Error'))

class Delete(View):

    def get(self, request):
        queryset = User.objects.filter(id=self.request.user.id)
        delete = get_object_or_404(queryset, id=self.request.user.id)

        return render(
            request,
            "delete.html",
            {
                "delete": delete,
            },
        )

    def post(self, request):
        queryset = User.objects.filter(id=self.request.user.id)
        delete = get_object_or_404(queryset, id=self.request.user.id)

        if delete:
            delete.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('home'), messages.add_message(request, messages.ERROR, 'Error')


class Settings(View):

    def get(self, request, *args, **kwargs):
        queryset = CwUsers.objects.filter(user_id=self.request.user.id)
        users = User.objects
        user = get_object_or_404(users, id=self.request.user.id)
        if not queryset:
            user_settings = CwUsers(cw_name=self.request.user.username, cw_id=0, user_id=user)
            user_settings.save()

        user_settings = get_object_or_404(queryset, user_id=self.request.user.id)

        return render(
            request,
            "settings.html",
            {
                "user_settings": user_settings,
                "user_form": CritticWarsForm(instance=user_settings),
            },
        )

    def post(self, request, *args, **kwargs):
        queryset = CwUsers.objects.filter(user_id=self.request.user.id)
        user_settings = get_object_or_404(queryset, user_id=self.request.user.id)
        user_form = CritticWarsForm(data=request.POST, instance=user_settings)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
        else:
            user_form = CritticWarsForm()

        return HttpResponseRedirect(reverse('home'), messages.add_message(request, messages.SUCCESS, 'User Settings Edited'))