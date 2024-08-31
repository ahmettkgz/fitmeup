from django.urls import path

from blogApp.views import BlogDeleteView
from .views import (QnaListView, QuestionsAndAnswersDetailsView, QuestionCreateView, QuestionUpdateView,
                    QuestionDeleteView, AnswerDeleteView)

# url patterns are created in here AnswerQuestionView

# he as_view() method is called to convert the MyView class into a callable view.
urlpatterns = [
    path("", QnaListView.as_view(), name="questionsandanswers"),
    path("newquestion/", QuestionCreateView.as_view(), name="question_create"),
    path("<int:pk>/update/", QuestionUpdateView.as_view(), name="question_update"),
    # primary key is necessary for the specific blog
    path("<int:pk>", QuestionsAndAnswersDetailsView.as_view(), name="questionandanswerdetails"),
    path("<int:pk>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
    path("<int:pk>/deleteanswer/", AnswerDeleteView.as_view(), name="answer_delete")
]
