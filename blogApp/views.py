from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from .models import BlogPost


# Create your views here.


class PostListView(ListView):
    model = BlogPost
    template_name = 'blogs.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class BlogDetailsView(View):
    def get(self, request, id):
        post = BlogPost.objects.get(id=id)
        context = {
            'post': post
        }
        return render(request, "blogs_details.html", context=context)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  # form_valid method on the parent class(super) before its running


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'blog_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # override the method before submission the post take that instance
        # and set the author equal to current user
        return super().form_valid(form)  # form_valid method on the parent class(super) before its running

    def test_func(self):
        post = self.get_object()  # to reach the current post
        if self.request.user == post.author:  # if the user that is login in already is the author, edit the page
            return True
        return False


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()  # to reach the current post
        if self.request.user == post.author:  # if the user that is login in already is the author, edit the page
            return True
        return False
