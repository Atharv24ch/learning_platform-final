from django.urls import path
from .views import GenerateQuizView, SubmitQuizView

urlpatterns = [
    path('generate/', GenerateQuizView.as_view(), name='generate-quiz'),
    path('submit/', SubmitQuizView.as_view(), name='submit-quiz'),
]
