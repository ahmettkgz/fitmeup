from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView

from users.models import Athlete, Chef, Other
from .forms import AnswerForm
from .models import Question, Answer


# Create your views here.
class QnaListView(ListView):
    model = Question
    template_name = 'questionandAnswers.html'
    context_object_name = 'questions'
    ordering = ['-date_posted']
    paginate_by = 5


class QuestionsAndAnswersDetailsView(View):
    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        answers = question.answer_set.all()  # Get all answers related to the question
        form = AnswerForm()
        myperson = None
        for my_class in [Athlete, Chef, Other]:
            try:
                myperson = my_class.objects.get(user=request.user)
                break
            except my_class.DoesNotExist:
                pass
        context = {
            'question': question,
            'answers': answers,
            'form': form,
            'myperson': myperson
        }
        return render(request, 'questionandAnswer_Details.html', context=context)

    def post(self, request, pk):
        question = Question.objects.get(pk=pk)
        answers = question.answer_set.all()

        form = AnswerForm(request.POST)  # Bind the form to the POST data
        if form.is_valid():
            text = form.cleaned_data['text']
            answer = Answer.objects.create(question=question, text=text, author=request.user)

        return redirect('questionandanswerdetails', pk=pk)  # Redirect to the same page after submitting


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'question_form.html'
    fields = ['title', 'details', 'recievers']

    def form_valid(self, form):
        form.instance.author = self.request.user  # override the method before submission the post take that instance
        # and set the author equal to current user
        return super().form_valid(form)  # form_valid method on the parent class(super) before its running


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'question_form.html'
    fields = ['title', 'details', 'recievers']

    def form_valid(self, form):
        form.instance.author = self.request.user  # override the method before submission the post take that instance
        # and set the author equal to current user
        return super().form_valid(form)  # form_valid method on the parent class(super) before its running

    def test_func(self):
        question = self.get_object()  # to reach the current post
        if self.request.user == question.author:  # if the user that is login in already is the author, edit the page
            return True
        return False


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/qa'
    template_name = 'question_confirm_delete.html'

    def test_func(self):
        post = self.get_object()  # to reach the current post
        if self.request.user == post.author:  # if the user that is login in already is the author, edit the page
            return True
        return False


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'answer_confirm_delete.html'

    def test_func(self):
        post = self.get_object()  # to reach the current post
        if self.request.user == post.author:  # if the user that is login in already is the author, edit the page
            return True
        return False

    def get_success_url(self):
        answer = self.get_object()
        return reverse_lazy('questionandanswerdetails', kwargs={'pk': answer.question.pk})
