import sys

from PyQt5 import QtWidgets

from task import load_file, run_creating_report_module

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.result_layout = QtWidgets.QVBoxLayout()

        self.initial_file_extension = QtWidgets.QComboBox()
        self.initial_file_extension.addItems(['csv', 'json'])

        self.project_name_group = QtWidgets.QHBoxLayout()
        self.project_name_label = QtWidgets.QLabel('Название проекта')
        self.project_name_edit = QtWidgets.QLineEdit()
        self.project_name_group.addWidget(self.project_name_label)
        self.project_name_group.addWidget(self.project_name_edit)

        self.task_name_group = QtWidgets.QHBoxLayout()
        self.task_name_label = QtWidgets.QLabel('Название задачи')
        self.task_name_edit = QtWidgets.QLineEdit()
        self.task_name_group.addWidget(self.task_name_label)
        self.task_name_group.addWidget(self.task_name_edit)

        self.task_number_group = QtWidgets.QHBoxLayout()
        self.task_number_label = QtWidgets.QLabel('Номер задачи')
        self.task_number_edit = QtWidgets.QSpinBox()
        self.task_number_edit.setMinimum(0)
        self.task_number_group.addWidget(self.task_number_label)
        self.task_number_group.addWidget(self.task_number_edit)

        self.date_group = QtWidgets.QHBoxLayout()
        self.date_label = QtWidgets.QLabel('Дата')
        self.date_edit = QtWidgets.QCalendarWidget()
        self.date_group.addWidget(self.date_label)
        self.date_group.addWidget(self.date_edit)

        self.effort_group = QtWidgets.QHBoxLayout()
        self.effort_label = QtWidgets.QLabel('Временные затраты')
        self.effort_value = QtWidgets.QLabel('0%')
        self.effort_edit = QtWidgets.QSlider(1)
        self.effort_edit.setMinimum(0)
        self.effort_edit.setMaximum(100)
        self.effort_group.addWidget(self.effort_label)
        self.effort_group.addWidget(self.effort_edit)
        self.effort_group.addWidget(self.effort_value)
        self.effort_edit.valueChanged.connect(self.effort_value_changed)

        self.table_view = QtWidgets.QTableView()

        self.file_name_group = QtWidgets.QHBoxLayout()
        self.file_name_label = QtWidgets.QLabel('Имя файла')
        self.file_name_edit = QtWidgets.QLineEdit()
        self.file_name_group.addWidget(self.file_name_label)
        self.file_name_group.addWidget(self.file_name_edit)

        self.extension = QtWidgets.QComboBox()
        self.extension.addItems(['csv', 'json'])

        self.create_report = QtWidgets.QPushButton('Создать отчёт')

        self.create_report.clicked.connect(self.create_report_click)

        self.result_layout.addWidget(self.initial_file_extension)
        self.result_layout.addLayout(self.project_name_group)
        self.result_layout.addLayout(self.task_name_group)
        self.result_layout.addLayout(self.task_number_group)
        self.result_layout.addLayout(self.date_group)
        self.result_layout.addLayout(self.effort_group)
        self.result_layout.addLayout(self.file_name_group)
        self.result_layout.addWidget(self.extension)
        self.result_layout.addWidget(self.create_report)

        self.setLayout(self.result_layout)

    def effort_value_changed(self):
        self.effort_value.setText(str(self.effort_edit.value()) + '%')

    def create_report_click(self):
        load_file(self.initial_file_extension.currentText())

        if (
                self.project_name_edit.text() == '' or
                self.task_name_edit.text() == '' or
                int(self.task_number_edit.value()) == 0 or
                self.file_name_edit.text() == ''
        ):
            dialog = QtWidgets.QDialog()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(QtWidgets.QLabel('Есть незаполненные поля'))
            dialog.setLayout(layout)
            dialog.exec_()
            return

        if '/' in self.file_name_edit.text() or '\\' in self.file_name_edit.text():
            dialog = QtWidgets.QDialog()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(QtWidgets.QLabel('Ошибка в имени файла'))
            dialog.setLayout(layout)
            dialog.exec_()
            return

        result = run_creating_report_module(
            self.project_name_edit.text(),
            self.task_name_edit.text(),
            int(self.task_number_edit.value()),
            self.date_edit.selectedDate().toPyDate(),
            float(self.effort_edit.value() / 100),
            self.file_name_edit.text(),
            self.extension.currentText(),
        )

        if not result:
            dialog = QtWidgets.QDialog()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(QtWidgets.QLabel('Отчёт не был создан, возможно неверно заполнены первые 3 поля'))
            dialog.setLayout(layout)
            dialog.exec_()
            return

        dialog = QtWidgets.QDialog()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel('Отчёт успешно создан'))
        dialog.setLayout(layout)
        dialog.exec_()


window = MainWindow()
window.show()

sys.exit(app.exec_())
