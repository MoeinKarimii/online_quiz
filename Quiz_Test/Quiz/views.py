import json

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Category, Questions, TheQuiz, QuestionItems


class ChooseCategory(View):

    def get(self, request, username):
        get_object_or_404(User, username=username)
        category_list = list(Category.objects.values('title'))
        polished_categories = []
        for elm in range(len(category_list)):
            polished_categories.append(list(category_list[elm].values())[0])
        return JsonResponse(polished_categories, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class GeneratingQuiz(View):
    @staticmethod
    def data_validator(data, fields):
        result = {}
        for i in range(len(fields)):
            if fields[i] not in data.keys():
                return JsonResponse(f'You forgot the {fields[i]} in json file', status=400)
            result.update({fields[i]: [data.get(f"{fields[i]}")]})
        return result

    def post(self, request, username):
        username = get_object_or_404(User, username=username)
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status': 'false', 'message': "send a json file please"}, status=400)
        data_prime = GeneratingQuiz.data_validator(data, ['category'])
        category = []
        # return HttpResponse(data_prime['category'])
        for i in range(len(data_prime["category"][0])):
            category.append(get_object_or_404(Category, title=data_prime["category"][0][i]))
        question = []
        # return HttpResponse(category[0])
        for i in range(len(category)):
            if i == 0:
                question.append(list(Questions.objects.filter(category__title=category[i])
                                     .order_by("?")[:(10 // len(category)) + (10 % len(category))]))
            else:
                question.append(list(Questions.objects.filter(category__title=category[i])
                                     .order_by("?")[:(10 // len(category))]))
        final_questions = []
        numbered_questions = {}
        counter = 1
        for i in range(len(question)):
            for j in range(len(question[i])):
                final_questions.append(['Question' + str(counter),
                                        str(question[i][j]),
                                        'a) ' + str(question[i][j].a),
                                        'b) ' + str(question[i][j].b),
                                        'c) ' + str(question[i][j].c),
                                        'd) ' + str(question[i][j].d)])
                numbered_questions.update({'Question' + str(counter): str(question[i][j].id)})
                counter += 1
        this_quiz = TheQuiz(username=username, )
        this_quiz.save()
        for i in range(len(final_questions)):
            question_items = QuestionItems(
                quiz_id=this_quiz,
                question_number=final_questions[i][0],
                question=get_object_or_404(Questions, id=numbered_questions[final_questions[i][0]]),
            )
            question_items.save()
        return JsonResponse([str(this_quiz)] + final_questions, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CheckAnswers(View):
    def post(self, request, username):
        username = get_object_or_404(User, username=username)
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status': 'false', 'message': "send a json file please"}, status=400)
        data_prime = GeneratingQuiz.data_validator(data, ['quiz_id', 'answers'])
        this_quiz = get_object_or_404(TheQuiz, id=int(data_prime['quiz_id'][0]))
        if this_quiz.done_status:
            return JsonResponse("You have taken this quiz before", status=400)
        if this_quiz.username != username:
            return JsonResponse("This Quiz is not assigned to this user", status=400)
        question = (QuestionItems.objects.filter(quiz_id=this_quiz).order_by())
        correct = 0
        wrong = 0
        not_answered = 0
        for elm in question:
            if elm.question_number in data_prime['answers'][0]:
                elm.user_answer = data_prime['answers'][0][elm.question_number]
                if elm.question.correct_answer == elm.user_answer:
                    correct += 1
                elif elm.user_answer == '' or None:
                    not_answered += 1
                else:
                    wrong += 1
            QuestionItems.save(elm)
        this_quiz.done_status = True
        this_quiz.result = {"correct": str(correct), "wrong": str(wrong), "not answered": str(not_answered),
                            "rate": "%"+str((correct / (correct + wrong + not_answered)) * 100)[:4]}
        this_quiz.save()
        return HttpResponse(f"correct answers: {correct} \nwrong answers: {wrong}\nnot answered: {not_answered}\n"
                            f"rate: {this_quiz.result['rate']}")


class UserRates(View):

    def get(self, request, username):
        username = get_object_or_404(User, username=username)
        results = TheQuiz.objects.filter(username=username)
        user_results = []
        for elm in results:
            user_results.append(elm.result)
        return JsonResponse(str(user_results), safe=False)

