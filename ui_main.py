import serial
import serial.tools.list_ports
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QMessageBox

# from database import JSONReader
from serial_worker import SerialReader
from printing import take_screenshot
from PyQt5.uic import loadUi


def motor_set_line_edit(line_edit_list, values):
    [line_edit.setText(val.split('@', 1)[1]) for line_edit, val in zip(line_edit_list, values) if '@' in val]





class Ui(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial_thread = SerialReader()  # Change this to your actual port
        self.Motor_number = 0

        self.setWindowState(Qt.WindowMaximized)
        loadUi(r'resource/Panel.ui', self)
        self.title_name_4.setText("Electro Power Pvt Ltd")
        self.value_validation()
        self.is_serial_port_connected = False
        self.is_application_running = False
        # -------------Refresh Button-------------------#
        self.refresh_ports()
        self.refrace_button.clicked.connect(self.refresh_ports)
        # -------------COM connect Button-------------------#
        self.read_button.setCheckable(True)
        self.read_button.toggled.connect(self.application_start)
        # -------------Application Start Button-------------------#
        self.connect_button.setCheckable(True)
        self.connect_button.toggled.connect(self.serial_connect_btn)
        self.btn_print.clicked.connect(self.print_btn_function)
        # self.btn_label_print.clicked.connect(self.label_print_btn_function)
        # self.btn_load.clicked.connect(self.load_data)
        # self.btn_save.clicked.connect(self.save_function)


        # -------------Clean Button-------------------#
        self.btn_clear.clicked.connect(self.clean_data)
        # -------------class variable-------------------#
        self.serial_port = None
        self.title_name_4.setText("Electro Power Pvt Ltd")
#------------------------- -------Line Edit List-------------------------------------
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

        self.motor_line_edits = [self.m1_lineEdits, self.m2_lineEdits, self.m3_lineEdits, self.m4_lineEdits]

        self.motor_serial_line_edits = [self.m1serial_no,self.m2serial_no,self.m3serial_no,self.m4serial_no]

    def show_time(self):
        current_time = QDateTime.currentDateTime()
        self.time_lebel.setText(current_time.toString("HH:mm:ss"))
        self.date_lebel.setText(current_time.toString("dd-MM-yyyy"))

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
    # """----------------------------------Motor Related function-------------------------------------------"""

    def fill_motor_serial_number(self, data):
        if self.is_application_running:
            if 0 <= self.Motor_number < len(self.motor_serial_line_edits):
                self.motor_serial_line_edits[self.Motor_number].setText(data)

    def fill_motor_data(self, data):
        if self.is_application_running:
            values = data.split('&')
            motor_set_line_edit(self.motor_line_edits[self.Motor_number], values)
            self.Motor_number = (self.Motor_number + 1) % (len(self.motor_line_edits))

    # """----------------------------------Serial Related function-------------------------------------------"""
    def serial_connect_btn(self, checked):
        if checked:
            self.connect_button.setText("Disconnect")
            self.connect_serial()
        else:
            self.connect_button.setText("Connect")
            if self.is_serial_port_connected:
                self.is_serial_port_connected = False
                self.serial_thread.stop()

    def connect_serial(self):
        port = self.comPort_box.currentText()
        baud = self.combox_baudrate.currentText()
        if not self.is_serial_port_connected:
            try:
                self.serial_thread = SerialReader()  # Change this to your actual port
                self.serial_thread.connect_serial(port, baud)
                self.serial_thread.data_received.connect(self.handle_received)
                self.serial_thread.data_received.connect(self.handle_error)
                self.serial_thread.start()
                self.is_serial_port_connected = True

            except serial.serialutil.SerialException as e:
                QMessageBox.critical(self, "Error", f"{e}")

    def refresh_ports(self):
        self.comPort_box.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comPort_box.addItem(port.device)

    def handle_received(self, data):
        print(data)
        try:
            if data["type"] == "Motor_Value":
                temp = data["Data"]
                self.serial_thread.save_motor_data(self.Motor_number)
                self.fill_motor_data(temp)
            elif data["type"] == "Motor_Serial":
                self.serial_thread.save_motor_serial(self.Motor_number)
                self.fill_motor_serial_number(data["Data"])
            elif data["type"] == "Company_Name":
                self.title_name_4.setText(data["content"])
            elif data["content"] == "START":
                self.read_button.setChecked(True)
            elif data["content"] == "STOP":
                self.read_button.setChecked(False)
            elif data["type"] == "print":
                file_name = data["name"]
                QMessageBox.information(self, "Information", f"File Name: {file_name} success fully saved \n File location : Record/Screen record.")
            #-----------------
            elif data["type"] == "Error":
                self.connect_button.setChecked(False)
                self.read_button.setChecked(False)
                QMessageBox.critical(self, "Error", data["message"])
            else:
                pass
        except KeyError:
            self.connect_button.setChecked(False)
            QMessageBox.critical(self, "Error", "incorrect Data")
    def handle_error(self, data):
        pass
# """--------------------------Application Related Function----------------------------------------------"""
    def application_start(self, checked):
        if checked:
            self.clean_data()
            self.read_button.setText("Stop")
            self.is_application_running = True
            if not self.is_serial_port_connected:

                self.connect_button.setChecked(True)
            self.show_time()
        else:
            self.read_button.setText("Start")
            self.is_application_running = False

    def print_btn_function(self):
        self.serial_thread.print_function()

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
        self.Motor_number = 0

    #"""----------------------------System Close related Function------------------------------------------"""
    def closeEvent(self, event):
        if self.is_serial_port_connected:
            self.serial_thread.stop()
            self.is_serial_port_connected = False
        # self.db.close()
        event.accept()

