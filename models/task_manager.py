# models/task_manager.py
from tasks.models import Task
from datetime import datetime

def get_recent_tasks(limit=10):
    return Task.objects.all().order_by('-created_at')[:limit]

def create_task(title: str, description: str = None, deadline: datetime = None):
    task = Task(
        title=title,
        description=description or None,
        deadline=deadline,
        priority='medium',
        status='pending'
    )
    task.save()
    return task