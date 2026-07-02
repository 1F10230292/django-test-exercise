from django.contrib import admin
from django.urls import path
from todo import views as todo_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", todo_views.index, name="index"),
    path("<int:task_id>/", todo_views.detail, name="detail"),
    path('task/<int:task_id>/close/', todo_views.close_task, name='close_task'),
    path("<int:task_id>/edit/", todo_views.edit, name="edit"),
    path('<int:task_id>/delete', todo_views.delete, name='delete'),
]
