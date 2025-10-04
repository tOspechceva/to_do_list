import os
import sys
import django
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent / "data"  
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")  
django.setup()


from tasks.models import Task  


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QCalendarWidget,
    QWidget, QVBoxLayout, QHBoxLayout, QDateTimeEdit, QLineEdit,
    QStackedWidget, QLabel, QTextEdit, QMessageBox
)
from PyQt6.QtCore import QSize, Qt
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")
        self.setMinimumSize(QSize(350, 450))

        self.stacked_widget = QStackedWidget()

        # === Страница 1: добавление задачи ===
        page1 = QWidget()
        layout1 = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(QSize(300, 200))

        self.time = QDateTimeEdit()
        self.time.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.time.setFixedSize(QSize(300, 40))

        self.calendar.selectionChanged.connect(self.update_datetime_from_calendar)
        self.time.dateTimeChanged.connect(self.update_calendar_from_datetime)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название задачи...")
        self.title_input.setFixedSize(QSize(300, 40))

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Описание (необязательно)")
        self.description_input.setFixedSize(QSize(300, 80))

        self.button_add = QPushButton("Добавить задачу")
        self.button_add.setFixedSize(QSize(300, 40))
        self.button_add.clicked.connect(self.add_task)

        layout1.addWidget(QLabel("Выберите дедлайн:"))
        layout1.addWidget(self.calendar)
        layout1.addWidget(self.time)
        layout1.addWidget(QLabel("Название:"))
        layout1.addWidget(self.title_input)
        layout1.addWidget(QLabel("Описание:"))
        layout1.addWidget(self.description_input)
        layout1.addWidget(self.button_add)
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        page1.setLayout(layout1)

        # === Страница 2: главная (список задач) ===
        page2 = QWidget()
        self.layout2 = QVBoxLayout()
        self.task_list_label = QLabel("Задачи загружаются...")
        self.task_list_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout2.addWidget(self.task_list_label)

        button_to_page1 = QPushButton("Добавить новую задачу")
        button_to_page1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.layout2.addWidget(button_to_page1)
        page2.setLayout(self.layout2)

        self.stacked_widget.addWidget(page1)  # индекс 0
        self.stacked_widget.addWidget(page2)  # индекс 1

        # Навигация
        nav_layout = QHBoxLayout()
        btn_to_main = QPushButton("Главная")
        btn_to_add = QPushButton("Добавить задачу")

        btn_to_main.clicked.connect(lambda: self.switch_to_main())
        btn_to_add.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        nav_layout.addWidget(btn_to_main)
        nav_layout.addWidget(btn_to_add)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(nav_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Загружаем задачи при запуске
        self.switch_to_main()

    def switch_to_main(self):
        self.load_tasks()
        self.stacked_widget.setCurrentIndex(1)

    def load_tasks(self):
        tasks = Task.objects.all().order_by('-created_at')[:10]  # последние 10 задач
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

    def add_task(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым!")
            return

        description = self.description_input.toPlainText().strip() or None
        deadline = self.time.dateTime().toPyDateTime()

        # Создаём задачу
        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            priority='medium',  # можно добавить выбор приоритета позже
            status='pending'
        )
        task.save()

        QMessageBox.information(self, "Успех", "Задача успешно добавлена!")
        self.title_input.clear()
        self.description_input.clear()
        self.load_tasks()  # обновляем список

    def update_datetime_from_calendar(self):
        selected_date = self.calendar.selectedDate()
        current_datetime = self.time.dateTime()
        new_datetime = current_datetime
        new_datetime.setDate(selected_date)
        self.time.setDateTime(new_datetime)

    def update_calendar_from_datetime(self):
        selected_date = self.time.date()
        self.calendar.setSelectedDate(selected_date)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())