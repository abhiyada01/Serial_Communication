# This is a sample Python script.
import sys
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextDocument, QIntValidator
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.uic import loadUi
import serial
import serial.tools.list_ports


def show_error_popup(content):
    # Create a QMessageBox
    error_popup = QMessageBox()
    error_popup.setIcon(QMessageBox.Critical)
    error_popup.setWindowTitle("Error")
    error_popup.setText(content)
    error_popup.setInformativeText("Please check and try again.")
    error_popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    error_popup.setDefaultButton(QMessageBox.Ok)
    error_popup.exec_()


def set_value(value, lineedit):
    tem = value.split('@')
    lineedit.setText(tem[1])


def set_name(value, lineedit):
    tem = value.split('@')
    lineedit.setText(tem[0])


class Ui(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowState(Qt.WindowMaximized)
        self.serial_port = None
        self.pre_config_data = None
        self.Motor_data = None
        loadUi('Panel.ui', self)
        # ------------Timer------------------------------
        self.timer = QTimer(self)

        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.read_serial)
        self.show_time()

        # ---------------COM Port------------------------
        self.refresh_ports()
        self.connect_button.clicked.connect(self.connect_serial)
        self.refrace_button.clicked.connect(self.refresh_ports)

        # ---------------Pre Configuration Data------------------------
        self.value_button_setting()
        self.value_validation()

        # -------------Start & Stop------------------
        self.read_button.clicked.connect(self.start_reading)

        # -------Load, Save, Print-------------------------------------
        self.btn_load.clicked.connect(self.load_data)
        self.btn_save.clicked.connect(self.save_content)
        self.btn_print.clicked.connect(self.print_content)
        # -------Line Edit List-------------------------------------
        self.m1_lineEdits = [self.m1_motor_lvs, self.m1_normal_voltage, self.m1motorhighvoltage, self.m1lvscurrent,
                             self.m1normalcurrent, self.m1highestcurrent, self.m1maxcurrent, self.m1lvswattage,
                             self.m1normalwattage, self.m1maxwattage, self.m1IRValue, self.m1lvskva, self.m1normalkva,
                             self.m1maximumkva, self.m1powerfactor, self.m1linefactor, self.m1linefrequency,
                             self.m1ibvalue, self.m1hvcurrent, self.m1HVtest, self.m1status]

        self.m2_lineEdits = [self.m2_motor_lvs, self.m2_normal_voltage, self.m2motorhighvoltage, self.m2lvscurrent,
                             self.m2normalcurrent, self.m2highestcurrent, self.m2maxcurrent, self.m2lvswattage,
                             self.m2normalwattage, self.m2maxwattage, self.m2IRValue, self.m2lvskva, self.m2normalkva,
                             self.m2maximumkva, self.m2powerfactor, self.m2linefactor, self.m2linefrequency,
                             self.m2ibvalue, self.m2hvcurrent, self.m2HVtest, self.m2status]

        self.m3_lineEdits = [self.m3_motor_lvs, self.m3_normal_voltage, self.m3motorhighvoltage, self.m3lvscurrent,
                             self.m3normalcurrent, self.m3highestcurrent, self.m3maxcurrent, self.m3lvswattage,
                             self.m3normalwattage, self.m3maxwattage, self.m3IRValue, self.m3lvskva, self.m3normalkva,
                             self.m3maximumkva, self.m3powerfactor, self.m3linefactor, self.m3linefrequency,
                             self.m3ibvalue, self.m3hvcurrent, self.m3HVtest, self.m3status]

        self.m4_lineEdits = [self.m4_motor_lvs, self.m4_normal_voltage, self.m4motorhighvoltage, self.m4lvscurrent,
                             self.m4normalcurrent, self.m4highestcurrent, self.m4maxcurrent, self.m4lvswattage,
                             self.m4normalwattage, self.m4maxwattage, self.m4IRValue, self.m4lvskva, self.m4normalkva,
                             self.m4maximumkva, self.m4powerfactor, self.m4linefactor, self.m4linefrequency,
                             self.m4ibvalue, self.m4hvcurrent, self.m4HVtest, self.m4status]

    def connect_serial(self):
        try:
            if self.serial_port:
                self.serial_port.close()
                self.serial_port = None
                self.connect_button.setText('Open Port')
                self.timer.stop()
            else:
                port = self.comPort_box.currentText()
                baud = self.combox_baudrate.currentText()
                self.serial_port = serial.Serial(port, baud, timeout=1)
                self.connect_button.setText('Close Port')
        except Exception as e:
            show_error_popup(e)

    def closeEvent(self, event):
        # Close the serial port when the app is closed
        if self.serial_port:
            self.serial_port.close()
        event.accept()

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    text = file.read()
                    self.text_edit.setText(text)
            except Exception as e:
                self.text_edit.setText(f"Error loading file: {e}")

    def read_serial(self):
        try:
            if self.serial_port and self.serial_port.in_waiting > 0:
                motor_data = self.serial_port.readline().decode('utf-8').rstrip()
                self.process_serial_data(motor_data)
        except Exception as e:
            show_error_popup(e)

    def refresh_ports(self):
        self.comPort_box.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comPort_box.addItem(port.device)

    def send_parameter(self, para_type, value):
        self.pre_config_data = f"${para_type}@{value}\n"
        self.send_serial()

    def send_group_parameter(self):
        if self.serial_port:
            self.send_parameter('v1', self.lineEdit_v1.text())
            self.send_parameter('v2', self.lineEdit_v2.text())
            self.send_parameter('v3', self.lineEdit_v3.text())
            self.send_parameter('v4', self.lineEdit_v4.text())

            self.send_parameter('c1', self.lineEdit_c1.text())
            self.send_parameter('c2', self.lineEdit_c2.text())
            self.send_parameter('c3', self.lineEdit_c3.text())
            self.send_parameter('c4', self.lineEdit_c4.text())

            self.send_parameter('w1', self.lineEdit_w1.text())
            self.send_parameter('w2', self.lineEdit_w2.text())
            self.send_parameter('w3', self.lineEdit_w3.text())
            self.send_parameter('w4', self.lineEdit_w4.text())
        else:
            show_error_popup("Connect to UART")

    def send_serial(self):
        if self.serial_port:
            self.serial_port.write(self.pre_config_data.encode('utf-8'))
        else:
            show_error_popup("Connect to UART")

    def start_reading(self):
        if self.serial_port:
            self.serial_port.reset_input_buffer()
            if self.read_button.text() == "START":
                self.show_time()
                self.timer.start(100)
                self.read_button.setText("STOP")
                self.test_status.setText("PENDING")
            else:
                self.timer.stop()
                self.read_button.setText("START")
                self.test_status.setText("STATUS")
        else:
            show_error_popup("Connect to UART")

    def stop_reading(self):
        self.timer.stop()

    def create_content(self):
        # Create a QTextDocument to format the content
        document = QTextDocument()
        # Collect the content from all QLineEdit widgets
        html_content = "<h2>LineEdit Contents</h2>"
        html_content += "<ul>"
        for line_edit in self.m1_lineEdits:
            text = line_edit.text()
            html_content += f"<li>{text}</li>"
        html_content += "</ul>"

        # Set the collected content as HTML to the QTextDocument
        document.setHtml(html_content)
        return document

    def print_content(self):
        if self.m1serial_no.text():
            if self.m1_lineEdits[0].text():
                # Create a QPrinter object
                printer = QPrinter(QPrinter.HighResolution)
                # Open a print dialog
                dialog = QPrintDialog(printer, self)
                if dialog.exec_() == QPrintDialog.Accepted:
                    # Print the QTextDocument using the printer
                    self.create_content().print_(printer)
            else:
                show_error_popup("Nothing to Print")
        else:
            show_error_popup("Enter motor serial number")

    def save_content(self):
        if self.m1serial_no.text():
            if self.m1_lineEdits[0].text():
                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)",
                                                           options=options)
                if file_path:
                    try:
                        # Open the file in write mode
                        with open(file_path, 'w') as file:
                            file.write(self.create_content().toPlainText())

                        # Show a success message
                        QMessageBox.information(self, "Success", "File saved successfully!")

                    except Exception as e:
                        # Show an error message if something goes wrong
                        QMessageBox.critical(self, "Error", f"An error occurred while saving the file:\n{e}")
            else:
                show_error_popup("Nothing to save")
        else:
            show_error_popup("Enter motor serial number")

    def show_time(self):
        current_time = QDateTime.currentDateTime()
        self.time_lebel.setText(current_time.toString("HH:mm:ss"))
        self.date_lebel.setText(current_time.toString("dd-MM-yyyy"))

    def value_button_setting(self):
        self.btn_v1.clicked.connect(lambda: self.send_parameter('v1', self.lineEdit_v1.text()))
        self.btn_v2.clicked.connect(lambda: self.send_parameter('v2', self.lineEdit_v2.text()))
        self.btn_v3.clicked.connect(lambda: self.send_parameter('v3', self.lineEdit_v3.text()))
        self.btn_v4.clicked.connect(lambda: self.send_parameter('v4', self.lineEdit_v4.text()))

        self.btn_c1.clicked.connect(lambda: self.send_parameter('c1', self.lineEdit_c1.text()))
        self.btn_c2.clicked.connect(lambda: self.send_parameter('c2', self.lineEdit_c2.text()))
        self.btn_c3.clicked.connect(lambda: self.send_parameter('c3', self.lineEdit_c3.text()))
        self.btn_c4.clicked.connect(lambda: self.send_parameter('c4', self.lineEdit_c4.text()))

        self.btn_w1.clicked.connect(lambda: self.send_parameter('w1', self.lineEdit_w1.text()))
        self.btn_w2.clicked.connect(lambda: self.send_parameter('w2', self.lineEdit_w2.text()))
        self.btn_w3.clicked.connect(lambda: self.send_parameter('w3', self.lineEdit_w3.text()))
        self.btn_w4.clicked.connect(lambda: self.send_parameter('w4', self.lineEdit_w4.text()))
        self.btn_V_Send.clicked.connect(self.send_group_parameter)

    def value_validation(self):
        # ---------------config check Port------------------------
        int_validator = QIntValidator(0, 100, self)  # Example range: 0 to 100
        self.lineEdit_v1.setValidator(int_validator)
        self.lineEdit_v2.setValidator(int_validator)
        self.lineEdit_v3.setValidator(int_validator)
        self.lineEdit_v4.setValidator(int_validator)
        self.lineEdit_c1.setValidator(int_validator)
        self.lineEdit_c2.setValidator(int_validator)
        self.lineEdit_c3.setValidator(int_validator)
        self.lineEdit_c4.setValidator(int_validator)
        self.lineEdit_w1.setValidator(int_validator)
        self.lineEdit_w2.setValidator(int_validator)
        self.lineEdit_w3.setValidator(int_validator)
        self.lineEdit_w4.setValidator(int_validator)

    def m1_set_line_edit(self, values):
        count = 0
        for line_edit in self.m1_lineEdits:
            set_value(values[count], line_edit)
            count += 1

    def m2_set_line_edit(self, values):
        count = 0
        for line_edit in self.m2_lineEdits:
            set_value(values[count], line_edit)
            count += 1

    def m3_set_line_edit(self, values):
        count = 0
        for line_edit in self.m3_lineEdits:
            set_value(values[count], line_edit)
            count += 1

    def m4_set_line_edit(self, values):
        count = 0
        for line_edit in self.m4_lineEdits:
            set_value(values[count], line_edit)
            count += 1

    def process_serial_data(self, data):
        # Assume data is a comma-separated string like "value1,value2,value3"
        values = data.split('#')
        if values[0] == "NM1":
            values = values[1].split('&')
            self.m1_set_line_edit(values)
        if values[0] == "NM2":
            values = values[1].split('&')
            self.m2_set_line_edit(values)
        if values[0] == "NM3":
            values = values[1].split('&')
            self.m3_set_line_edit(values)
        if values[0] == "NM4":
            values = values[1].split('&')
            self.m4_set_line_edit(values)


def application():
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    application()
