from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCalendarWidget, QDateTimeEdit,
    QLineEdit, QTextEdit, QPushButton, QLabel
)
from PyQt6.QtCore import QSize, Qt
from datetime import datetime

class AddTaskPage(QWidget):
    def __init__(self, on_task_added):
        super().__init__()
        self.on_task_added = on_task_added
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

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

        layout.addWidget(QLabel("Выберите дедлайн:"))
        layout.addWidget(self.calendar)
        layout.addWidget(self.time)
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.description_input)
        layout.addWidget(self.button_add)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

    def add_task(self):
        title = self.title_input.text().strip()
        if not title:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым!")
            return

        description = self.description_input.toPlainText().strip() or None
        deadline = self.time.dateTime().toPyDateTime()

        # Вызов внешней логики
        self.on_task_added(title, description, deadline)

        # Очистка полей
        self.title_input.clear()
        self.description_input.clear()

    def update_datetime_from_calendar(self):
        selected_date = self.calendar.selectedDate()
        current_datetime = self.time.dateTime()
        new_datetime = current_datetime
        new_datetime.setDate(selected_date)
        self.time.setDateTime(new_datetime)

    def update_calendar_from_datetime(self):
        selected_date = self.time.date()
        self.calendar.setSelectedDate(selected_date)