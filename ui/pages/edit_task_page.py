from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCalendarWidget, QDateTimeEdit,
    QLineEdit, QTextEdit, QPushButton, QLabel, QComboBox
)
from PyQt6.QtCore import QSize, Qt
from datetime import datetime


class EditTaskPage(QWidget):
    def __init__(self, task_id, task_data, on_task_updated):
        super().__init__()
        self.task_id = task_id
        self.on_task_updated = on_task_updated
        self.task_data = task_data
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        layout.addWidget(QLabel("<h3>Редактировать задачу</h3>"))

        # Календарь и время
        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(QSize(300, 200))

        self.time = QDateTimeEdit()
        self.time.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.time.setFixedSize(QSize(300, 40))

        self.calendar.selectionChanged.connect(self.update_datetime_from_calendar)
        self.time.dateTimeChanged.connect(self.update_calendar_from_datetime)

        # Приоритет
        layout.addWidget(QLabel("Приоритет:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItem("Низкий", "low")
        self.priority_combo.addItem("Средний", "medium")
        self.priority_combo.addItem("Высокий", "high")
        layout.addWidget(self.priority_combo)

        # Статус
        layout.addWidget(QLabel("Статус:"))
        self.status_combo = QComboBox()
        self.status_combo.addItem("В ожидании", "pending")
        self.status_combo.addItem("В работе", "in_progress")
        self.status_combo.addItem("Выполнено", "completed")
        layout.addWidget(self.status_combo)

        # Название
        layout.addWidget(QLabel("Название:"))
        self.title_input = QLineEdit(self.task_data.title)
        self.title_input.setFixedSize(QSize(300, 40))
        layout.addWidget(self.title_input)

        # Описание
        layout.addWidget(QLabel("Описание:"))
        self.description_input = QTextEdit(self.task_data.description or "")
        self.description_input.setFixedSize(QSize(300, 80))
        layout.addWidget(self.description_input)

        # Кнопка сохранения
        self.button_save = QPushButton("Сохранить изменения")
        self.button_save.setFixedSize(QSize(300, 40))
        self.button_save.clicked.connect(self.save_task)
        layout.addWidget(self.button_save)

        # Установка дедлайна
        if self.task_data.deadline:
            self.time.setDateTime(self.task_data.deadline)
            self.calendar.setSelectedDate(self.task_data.deadline.date())
        else:
            now = datetime.now()
            self.time.setDateTime(now)
            self.calendar.setSelectedDate(now.date())

        # Установка текущих значений приоритета и статуса
        priority_index = self.priority_combo.findData(self.task_data.priority)
        if priority_index != -1:
            self.priority_combo.setCurrentIndex(priority_index)

        status_index = self.status_combo.findData(self.task_data.status)
        if status_index != -1:
            self.status_combo.setCurrentIndex(status_index)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def save_task(self):
        title = self.title_input.text().strip()
        if not title:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым!")
            return

        description = self.description_input.toPlainText().strip() or None
        deadline = self.time.dateTime().toPyDateTime()

        # Получаем внутренние значения из комбо-боксов
        priority = self.priority_combo.currentData()
        status = self.status_combo.currentData()

        self.on_task_updated(self.task_id, title, description, deadline, priority, status)

    def update_datetime_from_calendar(self):
        selected_date = self.calendar.selectedDate()
        current_datetime = self.time.dateTime()
        new_datetime = current_datetime
        new_datetime.setDate(selected_date)
        self.time.setDateTime(new_datetime)

    def update_calendar_from_datetime(self):
        selected_date = self.time.date()
        self.calendar.setSelectedDate(selected_date)