import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox, \
    QGridLayout, QLineEdit, QComboBox
from PyQt5.QtGui import QIcon, QColor, QPalette, QPainter, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QSize


class StudyMateApp(QMainWindow):
    def __init__(self):
        self.pressure = {"atm": 101325,
                         "mmHg": 133.322,
                         "torr": 133.322,
                         'kPa': 1000,
                         'bar': 100000,
                         'decibar': 10000,
                         'millibar': 100,
                         'Pa': 1}
        self.volume = {'cm³': 0.000001,
                       'L': 0.001,
                       'mL': 0.000001,
                       'ft³': 0.02831685,
                       'in³': 0.000016387064,
                       'm³': 1}
        super().__init__()
        self.setWindowTitle("StudyMate")
        self.setWindowIcon(QIcon('rasm.png'))
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.create_main_window()

    def create_main_window(self):
        main_label = QLabel("Ideal Gas Law Calculator\nPV = nRT\n"
                            "P = pressure\nV = volume\nn = number of moles\nT = temperature\nR = gas constant")
        main_label.setAlignment(Qt.AlignCenter)
        main_label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold; color: #333333;}")
        self.layout.addWidget(main_label)

        grid_layout = QGridLayout()
        self.layout.addLayout(grid_layout)

        known_values_label = QLabel("Known Values:")
        known_values_label.setStyleSheet("QLabel {font-weight: bold; font-size: 14px;}")
        grid_layout.addWidget(known_values_label, 0, 0, 1, 3)

        pressure_label = QLabel("Pressure P:")
        pressure_label.setStyleSheet("QLabel {font-size: 12px;}")
        self.pressure_input = QLineEdit()
        self.pressure_input.setStyleSheet("QLineEdit {background-color: #f5f5f5; border: 1px solid #aaaaaa; "
                                          "padding: 5px;}")
        grid_layout.addWidget(pressure_label, 1, 0)
        self.pressure_units = QComboBox()
        self.pressure_units.addItems(["atm", "mmHg", "torr", "Pa", "kPa", "bar", "decibar", "millibar"])
        self.pressure_units.setStyleSheet("QComboBox {background-color: #ffffff; border: 1px solid #aaaaaa; "
                                           "padding: 5px;}")
        grid_layout.addWidget(self.pressure_units, 1, 2)
        grid_layout.addWidget(self.pressure_input, 1, 1)

        volume_label = QLabel("Volume V:")
        volume_label.setStyleSheet("QLabel {font-size: 12px;}")
        self.volume_input = QLineEdit()
        self.volume_input.setStyleSheet("QLineEdit {background-color: #f5f5f5; border: 1px solid #aaaaaa; "
                                         "padding: 5px;}")
        grid_layout.addWidget(volume_label, 2, 0)
        self.volume_units = QComboBox()
        self.volume_units.addItems(["cm³", "m³", "mL", "L", "ft³", "in³"])
        self.volume_units.setStyleSheet("QComboBox {background-color: #ffffff; border: 1px solid #aaaaaa; "
                                         "padding: 5px;}")
        grid_layout.addWidget(self.volume_units, 2, 2)
        grid_layout.addWidget(self.volume_input, 2, 1)

        moles_label = QLabel("Moles n:")
        moles_label.setStyleSheet("QLabel {font-size: 12px;}")
        self.moles_input = QLineEdit()
        self.moles_input.setStyleSheet("QLineEdit {background-color: #f5f5f5; border: 1px solid #aaaaaa; "
                                        "padding: 5px;}")
        grid_layout.addWidget(moles_label, 3, 0)
        self.moles_units = QLabel("mol")
        self.moles_units.setStyleSheet("QLabel {font-size: 12px;}")
        grid_layout.addWidget(self.moles_units, 3, 2)
        grid_layout.addWidget(self.moles_input, 3, 1)

        temperature_label = QLabel("Temperature T:")
        temperature_label.setStyleSheet("QLabel {font-size: 12px;}")
        self.temperature_input = QLineEdit()
        self.temperature_input.setStyleSheet("QLineEdit {background-color: #f5f5f5; border: 1px solid #aaaaaa; "
                                              "padding: 5px;}")
        grid_layout.addWidget(temperature_label, 4, 0)
        self.temperature_units = QComboBox()
        self.temperature_units.addItems(["°C", "°F", "K", "°R"])
        self.temperature_units.setStyleSheet("QComboBox {background-color: #ffffff; border: 1px solid #aaaaaa; "
                                               "padding: 5px;}")
        grid_layout.addWidget(self.temperature_units, 4, 2)
        grid_layout.addWidget(self.temperature_input, 4, 1)

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        calculate_button.setStyleSheet("QPushButton {background-color: #4CAF50; color: #ffffff; font-weight: bold; "
                                        "padding: 8px 16px; border: none; border-radius: 4px;}"
                                        "QPushButton:hover {background-color: #45a049;}")
        grid_layout.addWidget(calculate_button, 5, 0, 1, 3)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_inputs)
        clear_button.setStyleSheet("QPushButton {background-color: #f44336; color: #ffffff; font-weight: bold; "
                                    "padding: 8px 16px; border: none; border-radius: 4px;}"
                                    "QPushButton:hover {background-color: #d32f2f;}")
        grid_layout.addWidget(clear_button, 6, 0, 1, 3)

        self.result_label = QLabel("Result: ")
        self.result_label.setStyleSheet("QLabel {font-weight: bold; font-size: 14px;}")
        grid_layout.addWidget(self.result_label, 7, 0, 1, 3)
    def calculate(self):
        pressure = self.pressure_input.text()
        pu = self.pressure_units.currentText()
        volume = self.volume_input.text()
        vu = self.volume_units.currentText()
        moles = self.moles_input.text()
        tu = self.temperature_units.currentText()
        temperature = self.temperature_input.text()

        known_values = [pressure, volume, moles, temperature]
        known_count = sum(value != "" for value in known_values)

        if known_count != 3:
            QMessageBox.warning(self, "Input Error", "Please enter exactly three known values.")
            return

        try:
            pressure = float(pressure) if pressure else None
            volume = float(volume) if volume else None
            moles = float(moles) if moles else None
            temperature = float(temperature) if temperature else None
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")
            return

        # Calculate the missing value
        gas_constant = 8.314  # R value
        if pressure is None:
            volume *= self.volume[vu]
            temperature = self.toK(temperature, tu)
            pressure = (moles * gas_constant * temperature) / volume
            pressure /= self.pressure[pu]
            self.result_label.setText(f"Result: Pressure P = {pressure:.2f} {self.pressure_units.currentText()}")

        elif volume is None:
            temperature = self.toK(temperature, tu)
            pressure *= self.pressure[pu]
            volume = (moles * gas_constant * temperature) / pressure
            volume /= self.volume[vu]
            self.result_label.setText(f"Result: Volume V = {volume:.2f} {self.volume_units.currentText()}")

        elif moles is None:
            volume *= self.volume[vu]
            temperature = self.toK(temperature, tu)
            pressure *= self.pressure[pu]
            moles = (pressure * volume) / (gas_constant * temperature)
            self.result_label.setText(f"Result: Moles n = {moles:.2f} {self.moles_units.text()}")
        elif temperature is None:
            volume *= self.volume[vu]
            pressure *= self.pressure[pu]
            temperature = (pressure * volume) / (moles * gas_constant)
            temperature = self.fromK(temperature, tu)
            self.result_label.setText(f"Result: Temperature T = {temperature:.2f} {self.temperature_units.currentText()}")

    def toK(self, a, tu):
        if tu == 'K':
            return a
        elif tu == '°C':
            return a + 273.15
        elif tu == '°F':
            return (a - 32) / 1.8 + 273.15
        elif tu == '°R':
            return a / 1.8

    def fromK(self, a, tu):
        if tu == 'K':
            return a
        elif tu == '°C':
            return a - 273.15
        elif tu == '°F':
            return 1.8 * (a - 273) + 32
        elif tu == '°R':
            return 1.8 * a

    def clear_inputs(self):
        self.pressure_input.clear()
        self.volume_input.clear()
        self.moles_input.clear()
        self.temperature_input.clear()
        self.result_label.setText("Result: ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    study_mate_app = StudyMateApp()
    study_mate_app.show()
    sys.exit(app.exec_())
