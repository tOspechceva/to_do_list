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
    
def update_task(task_id: int, title: str, description: str = None, deadline: datetime = None, priority: str = 'medium', status: str = 'pending') -> bool:
    """Обновляет задачу по ID. Возвращает True при успехе."""
    try:
        task = Task.objects.get(id=task_id)
        task.title = title
        task.description = description or None
        task.deadline = deadline
        task.priority = priority
        task.status = status
        task.save()
        return True
    except Task.DoesNotExist:
        return False
    except Exception:
        return False

def get_task_by_id(task_id: int):
    """Получает задачу по ID."""
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None