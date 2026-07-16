from django.db import models
from django.utils import timezone


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#d84a4a")

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    label = models.ForeignKey(
        Label,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
