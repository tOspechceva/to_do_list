# ui/pages/task_list_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from models.task_manager import delete_task_by_id  # ← добавим эту функцию позже


class TaskListPage(QWidget):
    def __init__(self, on_add_task_clicked, on_task_deleted, on_task_clicked):
        super().__init__()
        self.on_add_task_clicked = on_add_task_clicked
        self.on_task_deleted = on_task_deleted
        self.on_task_clicked = on_task_clicked  # ← новое
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Прокручиваемая область для списка задач
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.tasks_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.tasks_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Кнопка "Добавить задачу"
        button_to_add = QPushButton("Добавить новую задачу")
        button_to_add.clicked.connect(self.on_add_task_clicked)

        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(button_to_add)

        self.setLayout(main_layout)

    def update_tasks_display(self, tasks):
        # Очистка текущего списка
        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not tasks:
            placeholder = QLabel("<h3>Нет задач</h3>")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tasks_layout.addWidget(placeholder)
        else:
            for task in tasks:
                task_widget = self.create_task_widget(task)
                self.tasks_layout.addWidget(task_widget)

        self.tasks_layout.addStretch()  # чтобы задачи не растягивались

# В методе create_task_widget в ui/pages/task_list_page.py

    def create_task_widget(self, task):
        widget = QFrame()
        widget.setFrameShape(QFrame.Shape.Box)
        layout = QHBoxLayout()

        # Кликабельная область задачи
        status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(task.status, "❓")
        deadline_str = task.deadline.strftime("%d.%m.%Y %H:%M") if task.deadline else "нет"
        priority_display = task.get_priority_display()

        text = f"<b>{status_icon} {task.title}</b><br>" \
            f"<small>Дедлайн: {deadline_str} | Приоритет: {priority_display}</small>"

        label = QLabel(text)
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setCursor(Qt.CursorShape.PointingHandCursor)  # курсор как на ссылке
        label.mousePressEvent = lambda e, t_id=task.id: self.on_task_clicked(t_id)  # ← обработчик клика

        # Кнопка удаления
        delete_btn = QPushButton("🗑️ Удалить")
        delete_btn.setFixedSize(100, 30)
        delete_btn.clicked.connect(lambda _, t_id=task.id: self.on_task_deleted(t_id))

        layout.addWidget(label)
        layout.addWidget(delete_btn)
        layout.setAlignment(delete_btn, Qt.AlignmentFlag.AlignTop)
        widget.setLayout(layout)
        return widget