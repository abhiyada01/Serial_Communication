import json

from PyQt5.QtWidgets import QFileDialog

json_file_path = r"resource/data_container.json"
output_file_path = r"resource/output.txt"

def convert_json_to_text():
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    lines = ["REPORT MOTOR PARAMETER MEASUREMENT", f"Material_Reference={data['header']['fields'][0]['data']}",
             f"Customer_Name={data['header']['fields'][1]['data']}"]

    date = data['header']['fields'][2]['data']
    time = data['header']['fields'][3]['data']
    lines.append(f"Date={date} Time={time}")

    for idx, motor in enumerate(data['motors'], start=1):
        lines.append(f"Motor{idx}")
        fields_dict = {field['label']: field['data'] for field in motor['fields']}
        lines.append(f"Motor_{idx}_Serial_Number={fields_dict.get('Serial No', '')}")
        lines.append(f"Motor LVS={fields_dict.get('Motor LVS', 0)}")
        lines.append(f"Moto Normal Voltage={fields_dict.get('Motor Voltage', 0)}")
        lines.append(f"Motor High Voltage={fields_dict.get('Motor High Voltage', 2)}")
        lines.append(f"LVS Current={fields_dict.get('L.V. Current', 0)}")
        lines.append(f"Normal Current={fields_dict.get('Normal Current', 0)}")
        lines.append(f"Highest Current={fields_dict.get('Highest Current', 0)}")
        lines.append(f"Max Current={fields_dict.get('Max Current', 0)}")
        lines.append(f"LVS Wattage={fields_dict.get('LVS Wattage', 0)}")
        lines.append(f"Normal Wattage={fields_dict.get('Normal Wattage', 0)}")
        lines.append(f"Max Wattage={fields_dict.get('Max Wattage', 0)}")
        lines.append(f"I. R. Value={fields_dict.get('Motor I.R. Value', 0)}")
        lines.append(f"LVS KVA={fields_dict.get('LVS KVA', 0)}")
        lines.append(f"Normal KVA={fields_dict.get('Normal KVA', 0)}")
        lines.append(f"Maximum KVA={fields_dict.get('Maximum KVA', 0)}")
        lines.append(f"Power factor={fields_dict.get('Power Factor', 0)}")
        lines.append(f"Line Factor={fields_dict.get('Line Factor', 0)}")
        lines.append(f"Line Frequency={fields_dict.get('Line Frequency', 0)}")
        lines.append(f"I. B. Value={fields_dict.get('I. B. Value', 0)}")
        lines.append(f"H. V. Current={fields_dict.get('H.V. Current', 0)}")
        lines.append(f"H.V. Test={fields_dict.get('H.V. Test', 0)}")
        lines.append(f"STATUS={fields_dict.get('STATUS', 'Pass')}")

    with open(output_file_path, 'w') as f:
        f.write("\n".join(lines))

    print(f"File saved to {output_file_path}")

#---------------------Loading function------------------------------
