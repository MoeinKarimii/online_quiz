from django.urls import path
from .views import ChooseCategory, GeneratingQuiz, CheckAnswers, UserRates

urlpatterns = [
    path('<str:username>/choose-category', ChooseCategory.as_view(), name='choose_category'),
    path('<str:username>/show-me-what-you-got', GeneratingQuiz.as_view(), name='GenerateQuiz'),
    path('<str:username>/here-is-the-result', CheckAnswers.as_view(), name='CheckAnswers'),
    path('<str:username>/my-rates', UserRates.as_view(), name='UserRates'),

]
