
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.title


ANSWER_KEYS = (
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
)


class Questions(models.Model):
    question_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    a = models.CharField(max_length=255, null=True)
    b = models.CharField(max_length=255, null=True)
    c = models.CharField(max_length=255, null=True)
    d = models.CharField(max_length=255, null=True)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_KEYS, default='a')

    def __str__(self):
        return self.question_description


class TheQuiz(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    done_status = models.BooleanField(default=False)
    result = models.JSONField(null=True)
    created_time = models.DateTimeField(default=timezone.now())


class QuestionItems(models.Model):
    quiz_id = models.ForeignKey(TheQuiz, on_delete=models.CASCADE)
    question_number = models.CharField(max_length=10, default='Question1')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=1, choices=ANSWER_KEYS, null=True)
