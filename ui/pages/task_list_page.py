# ui/pages/task_list_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class TaskListPage(QWidget):
    def __init__(self, on_add_task_clicked):
        super().__init__()
        self.on_add_task_clicked = on_add_task_clicked
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.task_list_label = QLabel("Задачи загружаются...")
        self.task_list_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.task_list_label)

        button_to_add = QPushButton("Добавить новую задачу")
        button_to_add.clicked.connect(self.on_add_task_clicked)
        layout.addWidget(button_to_add)

        self.setLayout(layout)

    def update_tasks_display(self, tasks):
        if tasks:
            text = "<h3>Ваши задачи:</h3>\n"
            for task in tasks:
                status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(task.status, "❓")
                deadline_str = task.deadline.strftime("%d.%m.%Y %H:%M") if task.deadline else "нет"
                text += f"<p><b>{status_icon} {task.title}</b><br>"
                text += f"<small>Дедлайн: {deadline_str} | Приоритет: {task.get_priority_display()}</small></p>"
        else:
            text = "<h3>Нет задач</h3>"
        self.task_list_label.setText(text)