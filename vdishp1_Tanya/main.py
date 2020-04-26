import sys

from PyQt5 import QtWidgets

from dataframe_to_qt import DataFrameModel
from task import *

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.result_layout = QtWidgets.QVBoxLayout()

        self.extension = QtWidgets.QComboBox()
        self.extension.addItems(['csv', 'json'])

        self.vehicle = QtWidgets.QComboBox()
        self.vehicle.addItems(['автобус', 'поезд'])

        self.leave_group = QtWidgets.QHBoxLayout()
        self.leave_label = QtWidgets.QLabel('Вокзал отправления')
        self.leave_edit = QtWidgets.QLineEdit()
        self.leave_group.addWidget(self.leave_label)
        self.leave_group.addWidget(self.leave_edit)

        self.arrival_group = QtWidgets.QHBoxLayout()
        self.arrival_label = QtWidgets.QLabel('Вокзал прибытия')
        self.arrival_edit = QtWidgets.QLineEdit()
        self.arrival_group.addWidget(self.arrival_label)
        self.arrival_group.addWidget(self.arrival_edit)

        self.cal_group = QtWidgets.QHBoxLayout()
        self.cal_label = QtWidgets.QLabel('Дата отправки')
        self.cal = QtWidgets.QCalendarWidget()
        self.cal_group.addWidget(self.cal_label)
        self.cal_group.addWidget(self.cal)

        self.weekend_setting = QtWidgets.QComboBox()
        self.weekend_setting.addItems(['все', 'только выходные', 'только '
                                                                 'будние'])

        self.time_start_group = QtWidgets.QHBoxLayout()
        self.time_start_label = QtWidgets.QLabel('Начало интервала времени: 0')
        self.time_start = QtWidgets.QSlider(1)
        self.time_start.setMinimum(0)
        self.time_start.setMaximum(24)
        self.time_start.valueChanged.connect(self.time_start_changed)
        self.time_start_group.addWidget(self.time_start_label)
        self.time_start_group.addWidget(self.time_start)

        self.time_end_group = QtWidgets.QHBoxLayout()
        self.time_end_label = QtWidgets.QLabel('Конец интервала времени: 24')
        self.time_end = QtWidgets.QSlider(1)
        self.time_end.setMinimum(0)
        self.time_end.setMaximum(24)
        self.time_end.setValue(24)
        self.time_end.valueChanged.connect(self.time_end_changed)
        self.time_end_group.addWidget(self.time_end_label)
        self.time_end_group.addWidget(self.time_end)

        self.approximation_group = QtWidgets.QHBoxLayout()
        self.approximation_label = QtWidgets.QLabel('Интервал апроксимации: 0')
        self.approximation = QtWidgets.QSlider(1)
        self.approximation.setMinimum(0)
        self.approximation.setMaximum(10)
        self.approximation.valueChanged.connect(self.approximation_changed)
        self.approximation_group.addWidget(self.approximation_label)
        self.approximation_group.addWidget(self.approximation)

        self.show_results = QtWidgets.QPushButton('Показать')
        self.show_results.clicked.connect(self.show_button_click)

        self.table_view = QtWidgets.QTableView()

        self.extension.currentTextChanged.connect(self.update_table)
        self.vehicle.currentTextChanged.connect(self.update_table)
        self.leave_edit.textChanged.connect(self.update_table)
        self.arrival_edit.textChanged.connect(self.update_table)
        self.cal.selectionChanged.connect(self.update_table)
        self.weekend_setting.currentTextChanged.connect(self.update_table)
        self.time_start.valueChanged.connect(self.update_table)
        self.time_end.valueChanged.connect(self.update_table)
        self.approximation.valueChanged.connect(self.update_table)

        self.result_layout.addWidget(self.extension)
        self.result_layout.addWidget(self.vehicle)
        self.result_layout.addLayout(self.leave_group)
        self.result_layout.addLayout(self.arrival_group)
        self.result_layout.addLayout(self.cal_group)
        self.result_layout.addWidget(self.weekend_setting)
        self.result_layout.addLayout(self.time_start_group)
        self.result_layout.addLayout(self.time_end_group)
        self.result_layout.addLayout(self.approximation_group)

        self.result_layout.addWidget(self.show_results)

        self.result_layout.addWidget(self.table_view)

        self.setLayout(self.result_layout)

        self.update_table()

    def time_start_changed(self):
        self.time_start_label.setText('Начало интервала времени: ' +
                                      str(self.time_start.value()))

    def time_end_changed(self):
        self.time_end_label.setText('Конец интервала времени: ' +
                                    str(self.time_end.value()))

    def approximation_changed(self):
        self.approximation_label.setText('Интервал апроксимации: ' +
                                         str(self.approximation.value()))

    def update_table(self):
        set_input_file(
            self.extension.currentText(),
            self.vehicle.currentText()
        )

        df = get_filtered_df(
            self.leave_edit.text(),
            self.arrival_edit.text(),
            self.cal.selectedDate(),
            self.weekend_setting.currentText(),
            self.time_start.value(),
            self.time_end.value(),
            self.approximation.value(),
            show_plots=False
        )

        table_model = DataFrameModel(df.reset_index())
        self.table_view.setModel(table_model)

    def show_button_click(self):
        get_filtered_df(
            self.leave_edit.text(),
            self.arrival_edit.text(),
            self.cal.selectedDate().toPyDate(),
            self.weekend_setting.currentText(),
            self.time_start.value(),
            self.time_end.value(),
            self.approximation.value()
        )


window = MainWindow()
window.show()

sys.exit(app.exec_())
