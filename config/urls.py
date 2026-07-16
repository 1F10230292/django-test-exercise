from django.contrib import admin
from django.urls import path
from todo import views as todo_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", todo_views.index, name="index"),
    path("labels/add/", todo_views.add_label, name="add_label"),
    path("labels/<int:label_id>/delete/", todo_views.delete_label, name="delete_label"),
    path("<int:task_id>/", todo_views.detail, name="detail"),
    path('task/<int:task_id>/close/', todo_views.close_task, name='close_task'),
    path("<int:task_id>/edit/", todo_views.edit, name="edit"),
    path('<int:task_id>/delete', todo_views.delete, name='delete'),
]
