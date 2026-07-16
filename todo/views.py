from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task, Label
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def index(request):
    if request.method == "POST":
        label = None
        label_id = request.POST.get("label")
        if label_id:
            label = Label.objects.filter(pk=label_id).first()
        task = Task(
            title=request.POST["title"],
            due_at=make_aware(parse_datetime(request.POST["due_at"])),
            label=label,
        )
        task.save()
    if request.GET.get("order") == "due":
        tasks = Task.objects.order_by("due_at")
    else:
        tasks = Task.objects.order_by("-posted_at")
    # tasks = Task.objects.all()

    # Filter tasks by label (e.g. ?label=3, or ?label=none for unlabeled).
    selected_label = request.GET.get("label")
    if selected_label == "none":
        tasks = tasks.filter(label__isnull=True)
    elif selected_label:
        tasks = tasks.filter(label_id=selected_label)

    labels = Label.objects.all()

    tasks_json = [
        {
            "id": task.id,
            "title": task.title,
            "due_at": task.due_at.isoformat() if task.due_at else None,
            "completed": task.completed,
            "label": task.label.name if task.label else None,
            "color": task.label.color if task.label else None,
        }
        for task in tasks
    ]

    context = {
        "tasks": tasks,
        "tasks_json": tasks_json,
        "labels": labels,
        "selected_label": selected_label,
    }
    return render(request, "todo/index.html", context)


def add_label(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        color = request.POST.get("color") or "#d84a4a"
        if name:
            Label.objects.create(name=name, color=color)
    return redirect("index")


def delete_label(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    label.delete()
    return redirect("index")


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
        task.title = request.POST.get("title")
        due_at = request.POST.get("due_at")
        if due_at:
            task.due_at = make_aware(parse_datetime(due_at))

        label_id = request.POST.get("label")
        if label_id:
            task.label = Label.objects.filter(pk=label_id).first()
        else:
            task.label = None

        task.save()
        return redirect("index")

    labels = Label.objects.all()
    return render(request, "todo/edit.html", {"task": task, "labels": labels})

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)
