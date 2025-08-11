import json
json_file_path = r"resource/data_container.json"

class JSONReader:
    def __init__(self):
        self.json_file_path = json_file_path
        self.json_data = None
        self.updated_json_data = None

    def read_json(self):
        with open(self.json_file_path, 'r') as json_file:
            self.json_data = json.load(json_file)
            # print(self.json_data['motors'])
            return self.json_data

    def write_json(self, updated_json):
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.updated_json_data, json_file, indent=4)


    def write_motor_data(self, motor_index,  motor_data):
        self.read_json()
        motor_index = motor_index + 1
        # Split and extract values
        # Split the serial data by '&'
        serial_items = motor_data.split('&')

        # Extract values from serial data (everything after '@')
        serial_values = []
        for item in serial_items:
            if '@' in item:
                value_part = item.split('@')[1]
                # Try to convert to int if possible, otherwise keep as string
                try:
                    serial_values.append(int(value_part))
                except ValueError:
                    serial_values.append(value_part)

        # Create a copy of the original JSON to avoid modifying the original
        updated_json = self.json_data

        # Counter to track position in serial_values
        value_index = 0

        # Update motor data
        for motor in updated_json['motors']:
            if motor['motor_id'] == motor_index:
                for field in motor['fields']:
                    if value_index < len(serial_values):
                        field['data'] = serial_values[value_index]
                        value_index += 1
        self.updated_json_data = updated_json
        return updated_json


    def write_motor_serial(self, motor_index,  serial_number):
        self.read_json()
        updated_json = self.json_data
        for motor in updated_json['motors']:
            if motor['motor_id'] == motor_index + 1:
                tstr = "Motor_"+ str(motor_index) + "_Serial_Number"
                motor[tstr] = serial_number
        self.updated_json_data = updated_json
        return updated_json

