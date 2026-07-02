from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def index(request):
    if request.method == "POST":
        task = Task(
            title=request.POST["title"],
            due_at=make_aware(parse_datetime(request.POST["due_at"])),
        )
        task.save()
    if request.GET.get("order") == "due":
        tasks = Task.objects.order_by("due_at")
    else:
        tasks = Task.objects.order_by("-posted_at")
    # tasks = Task.objects.all()

    context = {"tasks": tasks}
    return render(request, "todo/index.html", context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    context = {
        "task": task,
    }
    return render(request, "todo/detail.html", context)

def close_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('detail', task_id=task_id)
  
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.title = request.POST.get('title')
        due_at = request.POST.get('due_at')
        if due_at:
            task.due_at = due_at
        
        task.save()
        return redirect("index")
    
    return render(request, "todo/edit.html", {"task": task})

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)
