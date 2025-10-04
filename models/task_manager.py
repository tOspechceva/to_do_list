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

def delete_task_by_id(task_id: int) -> bool:
    """Удаляет задачу по ID. Возвращает True при успехе."""
    try:
        from tasks.models import Task
        task = Task.objects.get(id=task_id)
        task.delete()
        return True
    except Task.DoesNotExist:
        return False
    except Exception:
        return False