# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
)
from PyQt6.QtCore import QSize
from ui.pages.add_task_page import AddTaskPage
from ui.pages.task_list_page import TaskListPage
from models.task_manager import create_task, get_recent_tasks

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")
        self.setMinimumSize(QSize(350, 450))

        self.stacked_widget = QStackedWidget()

        # Создаём страницы
        self.task_list_page = TaskListPage(on_add_task_clicked=self.go_to_add_page)
        self.add_task_page = AddTaskPage(on_task_added=self.handle_add_task)

        self.stacked_widget.addWidget(self.add_task_page)   # index 0
        self.stacked_widget.addWidget(self.task_list_page)  # index 1

        # Навигация
        nav_layout = QHBoxLayout()
        btn_to_main = QPushButton("Главная")
        btn_to_add = QPushButton("Добавить задачу")

        btn_to_main.clicked.connect(self.go_to_main_page)
        btn_to_add.clicked.connect(self.go_to_add_page)

        nav_layout.addWidget(btn_to_main)
        nav_layout.addWidget(btn_to_add)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(nav_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Загружаем задачи и открываем главную
        self.go_to_main_page()

    def go_to_main_page(self):
        tasks = get_recent_tasks()
        self.task_list_page.update_tasks_display(tasks)
        self.stacked_widget.setCurrentIndex(1)

    def go_to_add_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def handle_add_task(self, title, description, deadline):
        from PyQt6.QtWidgets import QMessageBox
        try:
            create_task(title=title, description=description, deadline=deadline)
            QMessageBox.information(self, "Успех", "Задача успешно добавлена!")
            self.go_to_main_page()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить задачу: {e}")