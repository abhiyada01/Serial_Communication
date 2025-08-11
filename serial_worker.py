# serial_worker.py
from PyQt5.QtCore import QThread, pyqtSignal
import serial
from database import JSONReader
from printing import take_screenshot

class SerialReader(QThread):
    # data_received = pyqtSignal(object)
    data_received: pyqtSignal = pyqtSignal(object)
    error_occurred: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.baud_rate = None
        self.port_name = None
        self.serial_port = None
        self.running = False
        self.Serial_data = None

    def connect_serial(self, port, baud_rate):
        self.baud_rate = baud_rate
        self.port_name = port
        self.running = True


    def run(self):
        try:
            self.serial_port = serial.Serial(self.port_name, self.baud_rate, timeout=1)
            self.serial_port.reset_output_buffer()
            self.serial_port.reset_input_buffer()
            self.running = True
        except Exception as e:
            print(e)
            self.data_received.emit({"type": "Error", "message": "Serial Port Error"})
            return
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    raw = self.serial_port.readline().decode(errors='ignore').strip()
                    self.Serial_data = self.decode_data(raw)
                    self.reflect_data(self.Serial_data)
                self.msleep(100)
            except (serial.SerialException, OSError) as e:
                print(f"Serial Disconnected during running of serial port {e}")
                self.data_received.emit({"type": "Error", "message": "Serial Disconnected"})
                self.stop()
            except Exception as e:
                print(f"Unexpected Error during running of serial port {e}")
                self.data_received.emit({"type": "Error", "message": "Unexpected Error:"})
                self.stop()
    def reflect_data(self, data):
        self.data_received.emit(data)
    def decode_data(self, data):
        if data.startswith("START#"):
            self.send_data("START#ack")
            return {"type": "CMD", "content": data[:5].strip()}
        elif data.startswith("STOP#"):
            self.send_data("STOP#ack")
            return {"type": "CMD", "content": data[:4].strip()}
        elif data.startswith("COMPANY#"):
            return {"type": "Company_Name", "content": data[8:].strip()}
        elif data.startswith("NM#"):
            return {"type": "Motor_Value", "Data": data[3:].strip()}
        elif data.startswith("MotorSerial#"):
            return {"type": "Motor_Serial", "Data": data[12:].strip()}
        else:
            return None

    def save_motor_data(self, motor_number):
        j = JSONReader()
        temp = j.write_motor_data(motor_number, self.Serial_data["Data"])
        j.write_json(temp)

    def save_motor_serial(self, motor_number):
        j = JSONReader()
        temp = j.write_motor_serial(motor_number, self.Serial_data["Data"])
        j.write_json(temp)

    def send_data(self, data):
        self.serial_port.write((data + '\n').encode())

    def print_function(self):
        pdf_name = take_screenshot()
        f_str = {"type": "print", "name": pdf_name}
        self.reflect_data(f_str)

    def stop(self):
        self.running = False
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
        except Exception as e:
            print(e)
        self.quit()
        self.wait()


