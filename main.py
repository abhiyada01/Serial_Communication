# This is a sample Python script.
import sys
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QTextDocument, QDoubleValidator
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.uic import loadUi


def set_value(value, lineedit):
    tem = value.split('@')
    lineedit.setText(tem[1])


def set_name(value, lineedit):
    tem = value.split('@')
    lineedit.setText(tem[0])


def load_value(value, lineedit):
    # print(value)
    tem = value.split('=')
    lineedit.setText(tem[1])


class Ui(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowState(Qt.WindowMaximized)
        loadUi('Panel.ui', self)
        # -------------class variable-------------------#
        self.serial_port = None
        self.pre_config_data = None
        self.Motor_data = None
        self.Motor_number = 0
        self.run = False
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
        self.btn_V_Send.clicked.connect(self.send_group_parameter)
        self.value_validation()

        # -------------Start & Stop------------------
        self.read_button.clicked.connect(self.start_stop_program)

        # -------Load, Save, Print-------------------------------------
        self.btn_load.clicked.connect(self.load_data)
        self.btn_save.clicked.connect(self.save_function)
        self.btn_print.clicked.connect(self.print_function)
        self.btn_clear.clicked.connect(self.clean_data)
        # -------Line Edit List-------------------------------------
        self.m1_lineEdits = [self.m1_motor_lvs, self.m1_normal_voltage, self.m1motorhighvoltage, self.m1lvscurrent,
                             self.m1normalcurrent, self.m1highestcurrent, self.m1maxcurrent, self.m1lvswattage,
                             self.m1normalwattage, self.m1maxwattage, self.m1IRValue, self.m1lvskva, self.m1normalkva,
                             self.m1maximumkva, self.m1powerfactor, self.m1linefactor, self.m1linefrequency,
                             self.m1ibvalue, self.m1hvcurrent, self.m1HVtest, self.m1status]

        self.m1_labels = [self.m1lbl1, self.m1lbl2, self.m1lbl3, self.m1lbl4, self.m1lbl5, self.m1lbl6, self.m1lbl7,
                          self.m1lbl8, self.m1lbl9, self.m1lbl10, self.m1lbl11, self.m1lbl12, self.m1lbl13,
                          self.m1lbl14,
                          self.m1lbl15, self.m1lbl16, self.m1lbl17, self.m1lbl18, self.m1lbl19, self.m1lbl20,
                          self.m1lbl21]

        self.m2_labels = [self.m2lbl1, self.m2lbl2, self.m2lbl3, self.m2lbl4, self.m2lbl5, self.m2lbl6, self.m2lbl7,
                          self.m2lbl8, self.m2lbl9, self.m2lbl10, self.m2lbl11, self.m2lbl12, self.m2lbl13,
                          self.m2lbl14,
                          self.m2lbl15, self.m2lbl16, self.m2lbl17, self.m2lbl18, self.m2lbl19, self.m2lbl20,
                          self.m2lbl21,
                          self.m2lbl22]

        self.m3_labels = [self.m3lbl1, self.m3lbl2, self.m3lbl3, self.m3lbl4, self.m3lbl5, self.m3lbl6, self.m3lbl7,
                          self.m3lbl8, self.m3lbl9, self.m3lbl10, self.m3lbl11, self.m3lbl12, self.m3lbl13,
                          self.m3lbl14,
                          self.m3lbl15, self.m3lbl16, self.m3lbl17, self.m3lbl18, self.m3lbl19, self.m3lbl20,
                          self.m3lbl21,
                          self.m3lbl22]

        self.m4_labels = [self.m4lbl1, self.m4lbl2, self.m4lbl3, self.m4lbl4, self.m4lbl5, self.m4lbl6, self.m4lbl7,
                          self.m4lbl8, self.m4lbl9, self.m4lbl10, self.m4lbl11, self.m4lbl12, self.m4lbl13,
                          self.m4lbl14,
                          self.m4lbl15, self.m4lbl16, self.m4lbl17, self.m4lbl18, self.m4lbl19, self.m4lbl20,
                          self.m4lbl21,
                          self.m4lbl22]

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

        self.title_name_4.setText("Electro Power Pvt Ltd")

    def show_time(self):
        current_time = QDateTime.currentDateTime()
        self.time_lebel.setText(current_time.toString("HH:mm:ss"))
        self.date_lebel.setText(current_time.toString("dd-MM-yyyy"))

    def close_serial_connection(self):
        self.serial_port.close()
        self.serial_port = None
        self.connect_button.setText('Open Port')
        self.timer.stop()

    def open_serial_connection(self):
        port = self.comPort_box.currentText()
        baud = self.combox_baudrate.currentText()
        self.serial_port = serial.Serial(port, baud, timeout=1)
        self.connect_button.setText('Close Port')
        self.timer.start(100)

    def connect_serial(self):
        try:
            if self.serial_port:
                self.close_serial_connection()
            else:
                self.open_serial_connection()
        except Exception as errors:
            QMessageBox.critical(self, "Error", f"Select the COM Port {errors}")

    def refresh_ports(self):
        self.comPort_box.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comPort_box.addItem(port.device)

    def read_serial(self):
        try:
            if self.serial_port and self.serial_port.in_waiting > 0:
                read_data = self.serial_port.readline().decode('utf-8').rstrip()
                self.process_serial_data(read_data)
        except Exception as errors:
            QMessageBox.critical(self, "Error", f"An error occurred while reading the data:\n{errors}")

    def send_data_on_serial(self, data):
        if self.serial_port:
            self.serial_port.write(data.encode('utf-8'))
        else:
            QMessageBox.critical(self, "Error", "Connect to UART")

    def send_serial(self):
        if self.serial_port:
            self.serial_port.write(self.pre_config_data.encode('utf-8'))
        else:
            QMessageBox.critical(self, "Error", "Connect to UART")

    def send_parameter(self, para_type, value):

        self.pre_config_data = f"${para_type}@{value}"
        self.send_serial()

    def send_group_parameter(self):
        try:
            if self.serial_port:
                data = (f"$LCLS lcls@{self.lowcurrentlowspeed.text()}"
                        f"&HCLS@{self.highcurrentlowspeed.text()}"
                        f"&LCMS@{self.lowcurrentmedspeed.text()}"
                        f"&HCMS@{self.highcurrentmedspeed.text()}"
                        f"&LCHS@{self.lowcurrenthighspeed.text()}"
                        f"&HCHS@{self.highcurrenthighspeed.text()}"
                        f"&LCLR@{self.lowcurrentlockrotor.text()}"
                        f"&HCLR@{self.highcurrentlockrotor.text()}"
                        f"&LWLS@{self.lowwattagelowspeed.text()}"
                        f"&HWLS@{self.highwattagelowspeed.text()}"
                        f"&LWMS@{self.lowwattagemedspeed.text()}"
                        f"&HWMS@{self.highwattagemedspeed.text()}"
                        f"&LWHS@{self.lowwattagehighspeed.text()}"
                        f"&HWHS@{self.highwattagehighspeed.text()}"
                        f"&LWLR@{self.lowwattagelockrotor.text()}"
                        f"&HWHR@{self.highwattagelockrotor.text()}\n"
                        )
                self.send_data_on_serial(data)
            else:
                QMessageBox.critical(self, "Error", "Connect COM")
        except Exception as errors:
            QMessageBox.critical(self, "Critical", f"\n{errors}")

    def start_reading(self):
        try:
            if not self.run:
                self.serial_port.reset_input_buffer()
                self.connect_button.setEnabled(False)
                self.show_time()
                self.timer.start(100)
                self.read_button.setText("STOP")
                # self.test_status.setText("PENDING")
                self.run = True
                return True
            else:
                return False
        except Exception as e:
            QMessageBox.critical(self, "Critical", f"Fail to start\n{e}")
            return False

    def stop_reading(self):
        try:
            if self.run:
                self.timer.stop()
                self.connect_button.setEnabled(True)
                self.read_button.setText("START")
                self.run = False
                return True
            else:
                return False
        except Exception as e:
            QMessageBox.critical(self, "Critical", f"Fail to stop\n{e}")
            return False

    def start_stop_program(self):
        if self.serial_port:
            if self.run:
                self.stop_reading()
            else:
                self.start_reading()
        else:
            QMessageBox.critical(self, "Critical", "Connect to UART")
            return False

    def print_content(self):
        # Create a QTextDocument to format the content
        document = QTextDocument()
        # -------------------Motor 1 Detail----------------------

        html_content = f"<h2>{self.title_name_3.text()}</h2>"
        html_content += f"<p>Material Reference : = {self.material_lineEdit.text()}</p>"
        html_content += f"<p>Customer Name : = {self.customer_lineEdit.text()}</p>"
        html_content += f"<p>Date := {self.date_lebel.text()} Time : {self.time_lebel.text()} </p>"
        html_content += f"<h1>Motor 1</h1>"
        html_content += f"Motor 1 Serial Number: = {self.m1serial_no.text()}"
        html_content += "<ul>"
        for label, line_edit in zip(self.m1_labels, self.m1_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl} = {text}</p>"
        html_content += "</ul>"
        html_content += f"<p><br></p>"
        html_content += f"<h1>Motor 2</h1>"
        html_content += f"Motor 2 Serial Number: = {self.m2serial_no.text()}"
        html_content += "<ul>"
        for label, line_edit in zip(self.m2_labels, self.m2_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl} = {text}</p>"
        html_content += "</ul>"
        html_content += f"<p><br></p>"
        html_content += f"<h1>Motor 3</h1>"
        html_content += f"Motor 3 Serial Number: = {self.m3serial_no.text()}"
        html_content += "<ul>"
        for label, line_edit in zip(self.m3_labels, self.m3_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl} = {text}</p>"
        html_content += "</ul>"
        html_content += f"<p><br></p>"
        html_content += f"<h1>Motor 4</h1>"
        html_content += f"Motor 4 Serial Number: = {self.m4serial_no.text()}"
        html_content += "<ul>"
        for label, line_edit in zip(self.m4_labels, self.m4_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl} = {text}</p>"
        html_content += "</ul>"
        # Set the collected content as HTML to the QTextDocument
        document.setHtml(html_content)
        return document

    def print_function(self):
        if self.m1serial_no.text():
            if self.m1_lineEdits[0].text():
                # Create a QPrinter object
                printer = QPrinter(QPrinter.HighResolution)
                # Open a print dialog
                dialog = QPrintDialog(printer, self)
                if dialog.exec_() == QPrintDialog.Accepted:
                    # Print the QTextDocument using the printer
                    self.print_content().print_(printer)
            else:
                QMessageBox.critical(self, "Error", "Nothing to Print")
        else:
            QMessageBox.critical(self, "Error", "Enter motor serial number")

    def save_content(self):
        # Create a QTextDocument to format the content
        document = QTextDocument()
        # -------------------Motor 1 Detail----------------------

        html_content = f"<h2>{self.title_name_3.text()}</h2>"
        html_content += f"<p>Material_Reference={self.material_lineEdit.text()}</p>"
        html_content += f"<p>Customer_Name={self.customer_lineEdit.text()}</p>"
        html_content += f"<p>Date={self.date_lebel.text()} Time={self.time_lebel.text()} </p>"
        html_content += f"<h1>Motor1</h1>"
        html_content += f"Motor_1_Serial_Number={self.m1serial_no.text()}"
        for label, line_edit in zip(self.m1_labels, self.m1_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl}={text}</p>"
        html_content += f"<h1>Motor2</h1>"
        html_content += f"Motor_2_Serial_Number:={self.m2serial_no.text()}"
        for label, line_edit in zip(self.m2_labels, self.m2_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl}={text}</p>"
        html_content += f"<h1>Motor3</h1>"
        html_content += f"Motor_3_Serial_Number:={self.m3serial_no.text()}"
        for label, line_edit in zip(self.m3_labels, self.m3_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl}={text}</p>"
        html_content += f"<h1>Motor4</h1>"
        html_content += f"Motor_4_Serial_Number:={self.m4serial_no.text()}"
        for label, line_edit in zip(self.m4_labels, self.m4_lineEdits):
            text = line_edit.text()
            lbl = label.text()
            html_content += f"<p>{lbl}={text}</p>"
        # Set the collected content as HTML to the QTextDocument
        document.setHtml(html_content)
        return document

    def save_function(self):
        if self.m1serial_no.text() and self.m2serial_no.text() and self.m3serial_no.text() and self.m4serial_no.text():
            if self.m1_lineEdits[0].text():
                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)",
                                                           options=options)
                if file_path:
                    try:
                        # Open the file in write mode
                        with open(file_path, 'w') as file:
                            file.write(self.save_content().toPlainText())

                        # Show a success message
                        QMessageBox.information(self, "Success", "File saved successfully!")

                    except Exception as errors:
                        # Show an error message if something goes wrong
                        QMessageBox.critical(self, "Error", f"An error occurred while saving the file:\n{errors}")
            else:
                QMessageBox.critical(self, "Error", "Nothing to save")
        else:
            QMessageBox.critical(self, "Error", "Enter motor serial number")

    def load_content(self, text):
        temp = text.readline().strip()
        self.title_name_3.setText(temp)
        # #----------------------------------------------
        temp = text.readline().strip()
        # self.material_lineEdit.setText("dfcvgbh")
        load_value(temp, self.material_lineEdit)
        temp = text.readline().strip()
        load_value(temp, self.customer_lineEdit)
        temp = text.readline().strip().split(' ')
        load_value(temp[0], self.date_lebel)
        load_value(temp[1], self.time_lebel)
        temp = text.readline().strip()

        if temp == "Motor1":
            temp = text.readline().strip()
            load_value(temp, self.m1serial_no)

            for line_edit in self.m1_lineEdits:
                temp = text.readline().strip()
                load_value(temp, line_edit)

        temp = text.readline().strip()
        if temp == "Motor2":
            temp = text.readline().strip()
            load_value(temp, self.m2serial_no)
            for line_edit in self.m2_lineEdits:
                temp = text.readline().strip()
                load_value(temp, line_edit)

        temp = text.readline().strip()
        if temp == "Motor3":
            temp = text.readline().strip()
            load_value(temp, self.m3serial_no)
            for line_edit in self.m3_lineEdits:
                temp = text.readline().strip()
                load_value(temp, line_edit)

        temp = text.readline().strip()
        if temp == "Motor4":
            temp = text.readline().strip()
            load_value(temp, self.m4serial_no)
            for line_edit in self.m4_lineEdits:
                temp = text.readline().strip()
                load_value(temp, line_edit)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.load_content(file)
            except Exception as errors:
                QMessageBox.Critical(self, "Error", f"Error Found \n{errors}")

    def value_validation(self):
        # ---------------config check Port------------------------
        float_validator = QDoubleValidator(0.0, 100.0, 2, self)  # Example range: 0 to 100
        self.lowcurrentlowspeed.setValidator(float_validator)
        self.highcurrentlowspeed.setValidator(float_validator)
        self.lowcurrentmedspeed.setValidator(float_validator)
        self.highcurrentmedspeed.setValidator(float_validator)
        self.lowcurrenthighspeed.setValidator(float_validator)
        self.highcurrenthighspeed.setValidator(float_validator)
        self.lowcurrentlockrotor.setValidator(float_validator)
        self.highcurrentlockrotor.setValidator(float_validator)

        self.highwattagelockrotor.setValidator(float_validator)
        self.highwattagelowspeed.setValidator(float_validator)
        self.lowwattagemedspeed.setValidator(float_validator)
        self.highwattagemedspeed.setValidator(float_validator)
        self.lowwattagehighspeed.setValidator(float_validator)
        self.highwattagehighspeed.setValidator(float_validator)
        self.lowwattagelockrotor.setValidator(float_validator)
        self.highwattagelockrotor.setValidator(float_validator)

        self.ac_leakage.setValidator(float_validator)
        self.insulation.setValidator(float_validator)

    def m1_set_line_edit(self, values):
        count = 0
        for line_edit in self.m1_lineEdits:
            set_value(values[count], line_edit)
            count += 1
        # count = 0
        # for lbl_edit in self.m1_labels:
        #     set_name(values[count], lbl_edit)
        #     count += 1

    def m1_clear_line_edit(self):
        pass

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

    def fill_motor_data(self, data):
        if self.Motor_number == 0:
            values = data.split('&')
            self.m1_set_line_edit(values)
            self.Motor_number = 1
        elif self.Motor_number == 1:
            values = data.split('&')
            self.m2_set_line_edit(values)
            self.Motor_number = 2
        elif self.Motor_number == 2:
            values = data.split('&')
            self.m3_set_line_edit(values)
            self.Motor_number = 3
        elif self.Motor_number == 3:
            values = data.split('&')
            self.m4_set_line_edit(values)
            self.Motor_number = 0
        else:
            pass

    def fill_motor_serial_number(self, data):
        if self.Motor_number == 0:
            self.m1serial_no.setText(data)
        if self.Motor_number == 1:
            self.m2serial_no.setText(data)
        if self.Motor_number == 2:
            self.m3serial_no.setText(data)
        if self.Motor_number == 3:
            self.m4serial_no.setText(data)

    def clean_data(self):
        self.m1serial_no.setText(" ")
        self.m2serial_no.setText(" ")
        self.m3serial_no.setText(" ")
        self.m4serial_no.setText(" ")
        for line_edit in self.m1_lineEdits:
            line_edit.setText(" ")
        for line_edit in self.m2_lineEdits:
            line_edit.setText(" ")
        for line_edit in self.m3_lineEdits:
            line_edit.setText(" ")
        for line_edit in self.m4_lineEdits:
            line_edit.setText(" ")

    def process_serial_data(self, data):
        # Assume data is a comma-separated string like "value1,value2,value3"
        values = data.split('#')
        if values[0] == "NM":
            self.fill_motor_data(values[1])

        # MotorSerial#1234567
        if values[0] == "MotorSerial":
            self.fill_motor_serial_number(values[1])

        if values[0] == "START":
            if values[1] == "req":
                if self.start_reading():  # CMD = "START#req"
                    self.send_data_on_serial("START#ack")
        if values[0] == "STOP":  # CMD = "STOP#req"
            if values[1] == "req":
                if self.stop_reading():
                    self.send_data_on_serial("STOP#ack")
        # COMPANY#name
        if values[0] == "COMPANY":
            self.title_name_4.setText(values[1])


def application():
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    application()
