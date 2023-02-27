from django.http import HttpResponse
from . import tasks

from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from main.tasks import cpu_task

# Create your views here.

def home(request):
    # вызываем task
    # .delay() - выставить задачу
    # в очередь в асинхронном режиме
    tasks.download_a_cat.delay()
    return HttpResponse('<h1>Загружаю фото кота!!!!</h1>')

# endpoint, вызывает функцию постановки задачи
# возвращает id задачи
class TaskSetter(APIView):
    # authentication_classes = [authentication.]
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # вызываем задачу с методом .delay()
        # для постановки задачи, асинхронного выполнения
        res = tasks.cpu_task.delay()
        # вернем id задачи
        return Response(res.id)

# запрашивает статус задачи по id
class TaskGetter(APIView):
    # authentication_classes = [authentication.]
    def get(self, request, format=None):
        # получаем id задачи
        task_id = request.GET.get('task_id')
        if task_id:
            res = AsyncResult(task_id)
            # вернем статус задачи
            return Response(res.state)
        return Response("no id was provided")

