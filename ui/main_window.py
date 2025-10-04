# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
)
from PyQt6.QtCore import QSize
from ui.pages.add_task_page import AddTaskPage
from ui.pages.task_list_page import TaskListPage
from ui.pages.edit_task_page import EditTaskPage
from models.task_manager import (
    create_task,
    get_recent_tasks,
    delete_task_by_id,
    get_task_by_id,
    update_task
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список задач")
        self.setMinimumSize(QSize(400, 500))

        # Стек страниц
        self.stacked_widget = QStackedWidget()

        # Страницы
        self.edit_task_page = None  # будет создаваться динамически

        # Главная страница списка задач
        self.task_list_page = TaskListPage(
            on_add_task_clicked=self.go_to_add_page,
            on_task_deleted=self.handle_delete_task,
            on_task_clicked=self.go_to_edit_page
        )

        # Страница добавления задачи
        self.add_task_page = AddTaskPage(on_task_added=self.handle_add_task)

        # Добавляем основные страницы в стек
        self.stacked_widget.addWidget(self.task_list_page)   # index 0
        self.stacked_widget.addWidget(self.add_task_page)    # index 1

        # Навигационные кнопки
        nav_layout = QHBoxLayout()
        btn_to_main = QPushButton("Главная")
        btn_to_add = QPushButton("Добавить задачу")

        btn_to_main.clicked.connect(self.go_to_main_page)
        btn_to_add.clicked.connect(self.go_to_add_page)

        nav_layout.addWidget(btn_to_main)
        nav_layout.addWidget(btn_to_add)

        # Основной layout
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
        self.stacked_widget.setCurrentWidget(self.task_list_page)

    def go_to_add_page(self):
        self.stacked_widget.setCurrentWidget(self.add_task_page)

    def go_to_edit_page(self, task_id: int):
        task = get_task_by_id(task_id)
        if not task:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", "Задача не найдена.")
            return

        # Удаляем предыдущую страницу редактирования (если есть)
        if self.edit_task_page:
            self.edit_task_page.deleteLater()

        # Создаём новую страницу редактирования
        self.edit_task_page = EditTaskPage(
            task_id=task_id,
            task_data=task,
            on_task_updated=self.handle_update_task
        )
        self.stacked_widget.addWidget(self.edit_task_page)
        self.stacked_widget.setCurrentWidget(self.edit_task_page)

    def handle_add_task(self, title, description, deadline):
        from PyQt6.QtWidgets import QMessageBox
        try:
            create_task(title=title, description=description, deadline=deadline)
            QMessageBox.information(self, "Успех", "Задача успешно добавлена!")
            self.go_to_main_page()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить задачу: {e}")

    def handle_delete_task(self, task_id: int):
        from PyQt6.QtWidgets import QMessageBox
        success = delete_task_by_id(task_id)
        if success:
            QMessageBox.information(self, "Удалено", "Задача успешно удалена.")
            self.go_to_main_page()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить задачу.")

    def handle_update_task(self, task_id, title, description, deadline, priority, status):
        from PyQt6.QtWidgets import QMessageBox
        success = update_task(task_id, title, description, deadline, priority, status)
        if success:
            QMessageBox.information(self, "Успех", "Задача обновлена!")
            self.go_to_main_page()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить задачу.")