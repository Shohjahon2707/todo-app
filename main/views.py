from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.utils.dateparse import parse_datetime
# Create your views here.
from django.utils import timezone

def task_list(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'main/list.html', context)

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        completed = 'completed' in request.POST
        deadline_str = request.POST.get('deadline')
        deadline = parse_datetime(deadline_str) if deadline_str else None

        Task.objects.create(
            title=title,
            completed=completed,
            deadline=deadline
        )
        return redirect('task_list')

    return render(request, 'main/create.html')


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')
    return render(request, 'main/update.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'main/delete_confirm.html', {'task': task})
