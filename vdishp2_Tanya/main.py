import sys

from PyQt5 import QtWidgets

from utils import DataFrameModel
from task import load_file, run_statistics_module

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.result_layout = QtWidgets.QVBoxLayout()

        self.extension = QtWidgets.QComboBox()
        self.extension.addItems(['csv', 'json'])

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

        self.effort_group = QtWidgets.QHBoxLayout()
        self.effort_label = QtWidgets.QLabel('Трудоёмкость')
        self.effort_edit = QtWidgets.QSpinBox()
        self.effort_edit.setMinimum(0)
        self.effort_group.addWidget(self.effort_label)
        self.effort_group.addWidget(self.effort_edit)

        self.executor_group = QtWidgets.QHBoxLayout()
        self.executor_label = QtWidgets.QLabel('Исполнитель')
        self.executor_edit = QtWidgets.QLineEdit()
        self.executor_group.addWidget(self.executor_label)
        self.executor_group.addWidget(self.executor_edit)

        self.show_unassigned = QtWidgets.QCheckBox('Показывать не назначенные')

        self.sorting_field_group = QtWidgets.QHBoxLayout()
        self.sorting_field_label = QtWidgets.QLabel('Поле сортировки')
        self.sorting_field = QtWidgets.QComboBox()
        self.sorting_field.addItems(['', 'название проекта', 'название задачи',
                                     'id задачи', 'трудоёмкость', 'исполнитель'])
        self.sorting_field_group.addWidget(self.sorting_field_label)
        self.sorting_field_group.addWidget(self.sorting_field)

        self.sorting_type_group = QtWidgets.QHBoxLayout()
        self.sorting_type_label = QtWidgets.QLabel('Поле сортировки')
        self.sorting_type = QtWidgets.QComboBox()
        self.sorting_type.addItems(['<', '>'])
        self.sorting_type_group.addWidget(self.sorting_type_label)
        self.sorting_type_group.addWidget(self.sorting_type)

        self.show_results = QtWidgets.QPushButton('Показать графики')
        self.table_view = QtWidgets.QTableView()

        self.extension.currentTextChanged.connect(self.update_table)
        self.project_name_edit.textChanged.connect(self.update_table)
        self.task_name_edit.textChanged.connect(self.update_table)
        self.task_number_edit.valueChanged.connect(self.update_table)
        self.effort_edit.valueChanged.connect(self.update_table)
        self.executor_edit.textChanged.connect(self.update_table)
        self.show_unassigned.stateChanged.connect(self.update_table)
        self.sorting_field.currentTextChanged.connect(self.update_table)
        self.sorting_type.currentTextChanged.connect(self.update_table)

        self.show_results.clicked.connect(self.show_button_click)

        self.result_layout.addWidget(self.extension)
        self.result_layout.addLayout(self.project_name_group)
        self.result_layout.addLayout(self.task_name_group)
        self.result_layout.addLayout(self.task_number_group)
        self.result_layout.addLayout(self.effort_group)
        self.result_layout.addLayout(self.executor_group)
        self.result_layout.addWidget(self.show_unassigned)
        self.result_layout.addLayout(self.sorting_field_group)
        self.result_layout.addLayout(self.sorting_type_group)

        self.result_layout.addWidget(self.show_results)
        self.result_layout.addWidget(self.table_view)

        self.table_view.setSortingEnabled(False)

        self.setLayout(self.result_layout)
        self.update_table()

    def update_table(self):
        load_file(self.extension.currentText())

        df = run_statistics_module(
            self.project_name_edit.text(),
            self.task_name_edit.text(),
            int(self.task_number_edit.text() or 0),
            int(self.effort_edit.text() or 0),
            self.executor_edit.text(),
            self.show_unassigned.isChecked(),
            self.sorting_field.currentText(),
            self.sorting_type.currentText()
        )

        table_model = DataFrameModel(df.reset_index())
        self.table_view.setModel(table_model)
        
    def show_button_click(self):
        run_statistics_module(
            self.project_name_edit.text(),
            self.task_name_edit.text(),
            int(self.task_number_edit.text()),
            int(self.effort_edit.text()),
            self.executor_edit.text(),
            self.show_unassigned.isChecked(),
            self.sorting_field.currentText(),
            self.sorting_type.currentText(),
            True
        )


window = MainWindow()
window.show()

sys.exit(app.exec_())
