from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView

from users.models import Athlete, Chef, Other
from .models import AthleteQuote


class AthletesQuotesView(ListView):
    model = AthleteQuote
    template_name = 'athletesquotes.html'
    context_object_name = 'posts'
    ordering = ['-posting_date']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myperson'] = None

        if self.request.user.is_authenticated:
            try:
                context['myperson'] = Athlete.objects.get(user=self.request.user)
            except Athlete.DoesNotExist:
                pass

        return context


class AthleteQuoteDetailsView(LoginRequiredMixin, View):
    def get(self, request, id):
        post = AthleteQuote.objects.get(id=id)
        myperson2 = None
        for my_class in [Athlete, Chef, Other]:
            try:
                myperson2 = my_class.objects.get(user=request.user)
                break
            except my_class.DoesNotExist:
                pass

        context = {
            'post': post,
            'myperson2': myperson2
        }
        return render(request, "quote_details.html", context=context)


class AthleteQuoteCreateView(LoginRequiredMixin, CreateView):
    model = AthleteQuote
    template_name = 'quote_form.html'
    fields = ['inspiration']

    def form_valid(self, form):
        form.instance.author = self.request.user

        # Set the athlete field to the currently logged-in athlete
        try:
            athlete = Athlete.objects.get(user=self.request.user)
            form.instance.athlete = athlete
        except Athlete.DoesNotExist:
            pass

        return super().form_valid(form)


class AthleteQuoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AthleteQuote
    template_name = 'quote_form.html'
    fields = ['inspiration']

    def form_valid(self, form):
        form.instance.author = self.request.user  # override the method before submission the post take that instance
        # and set the author equal to current user
        return super().form_valid(form)  # form_valid method on the parent class(super) before its running

    def test_func(self):
        post = self.get_object()  # to reach the current post
        if self.request.user == post.athlete.user:  # if the user that is login in already is the author, edit the page
            return True
        return False


class AthleteQuoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AthleteQuote
    success_url = '/quotes'
    template_name = 'quote_confirm_delete.html'

    def test_func(self):
        post = self.get_object()  # to reach the current post
        if self.request.user == post.athlete.user:  # if the user that is login in already is the author, edit the page
            return True
        return False
