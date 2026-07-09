from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task
from django.urls import reverse
from datetime import datetime


# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)


class TaskModelTestCase(TestCase):
    def test_create_task1(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title="task1", due_at=due)
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, "task1")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)

    def test_create_task2(self):
        task = Task(title="task2")
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertAlmostEqual(task.title, "task2")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, None)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title="task1", due_at=due)
        task.save()

        self.assertFalse(task.is_overdue(current))

    def test_is_overdue_past(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        task = Task(title="task1", due_at=due)
        task.save()

        self.assertTrue(task.is_overdue(current))

    def test_is_overdue_none(self):
        current = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        task = Task(title="task2")
        task.save()

        self.assertFalse(task.is_overdue(current))


class TodoViewTestCase(TestCase):
    def test_index_get(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/index.html")
        self.assertEqual(len(response.context["tasks"]), 0)

    def test_index_post(self):
        client = Client()
        data = {"title": "Test Task", "due_at": "2024-06-30 23:59:59"}
        response = client.post("/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/index.html")
        self.assertEqual(len(response.context["tasks"]), 1)

    def test_index_get_order_post(self):
        task1 = Task(title="task1", due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title="task2", due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = Client()
        response = client.get("/?order=post")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/index.html")
        self.assertEqual(response.context["tasks"][0], task2)
        self.assertEqual(response.context["tasks"][1], task1)

    def test_index_get_order_due(self):
        task1 = Task(title="task1", due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title="task2", due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = Client()
        response = client.get("/?order=due")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/index.html")
        self.assertEqual(response.context["tasks"][0], task1)
        self.assertEqual(response.context["tasks"][1], task2)

    def test_detail_get_success(self):
        task = Task(title="task1", due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()
        response = client.get("/{}/".format(task.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/detail.html")
        self.assertEqual(response.context["task"], task)

    def test_detil_get_fail(self):
        client = Client()
        response = client.get("/1/")

        self.assertEqual(response.status_code, 404)
    
    def test_close_task_success(self):
        task = Task(title="Test Close Task", completed=False)
        task.save()
        
        client = Client()
        response = client.get(reverse('close_task', args=[task.pk]))

        expected_redirect_url = reverse('detail', args=[task.pk])
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_close_task_fail_not_found(self):
        client = Client()
        response = client.get(reverse('close_task', args=[999]))

    def test_edit_get_success(self):
        task = Task(title="task1", due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()
        response = client.get("/{}/edit/".format(task.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/edit.html")
        self.assertEqual(response.context["task"], task)

    def test_edit_post_updates_task_and_redirects(self):
        task = Task(title="old title", due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()
        response = client.post(
            "/{}/edit/".format(task.pk),
            {"title": "updated title", "due_at": "2024-08-01 00:00:00"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

        task.refresh_from_db()
        self.assertEqual(task.title, "updated title")
        local_due_at = timezone.localtime(task.due_at)
        self.assertEqual(local_due_at.strftime("%Y-%m-%d %H:%M:%S"), "2024-08-01 00:00:00")
        
    def test_delete_task_success(self):
        task = Task(title="task1", due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()

        response = client.get("/{}/delete".format(task.pk))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

        follow_response = client.get(response.url)
        self.assertEqual(follow_response.status_code, 200)
        self.assertEqual(len(follow_response.context["tasks"]), 0)

    def test_delete_task_fail(self):
        client = Client()
        response = client.get("/1/delete")

        self.assertEqual(response.status_code, 404)
