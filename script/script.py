import time
import requests
import re
from datetime import datetime
file_path = 'cnc.txt'

api_url = 'http://127.0.0.1:5000/updatemachine'

# JWT of the user
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDIzNDM1MSwianRpIjoiMWJkNjllNGUtYTM5OS00NzdlLWJlZTQtZjlhNTE0M2FlMGExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6Im1hbmFnZXIiLCJyb2xlIjoiTWFuYWdlciJ9LCJuYmYiOjE3MjQyMzQzNTEsImNzcmYiOiI4NzEzN2FjYi0xODIxLTQ3MmMtYTYzYy0yNTZlZTk4NzRkYWUifQ.F-o5hpaCOMUA90NevUTNuyVj9O6tLYYonTPHi2CqDls'

def parse_cnc_file(file_path):
    machines = []   
    current_machine = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Name"):
                if current_machine:
                    machines.append(current_machine)
                    current_machine = {}
                current_machine['name'] = line.split()[1]
            elif line.startswith("acceleration"):
                current_machine['acceleration'] = float(line.split()[1].replace(',', '.'))
            elif line.startswith("actual_position"):
                current_machine['actual_position'] = [float(x.replace(',', '.')) for x in line.split()[1:]]
            elif line.startswith("distance_to_go"):
                current_machine['distance_to_go'] = [float(x.replace(',', '.')) for x in line.split()[1:]]
            elif line.startswith("homed"):
                current_machine['homed'] = [bool(int(x)) for x in line.split()[1:]]
            elif line.startswith("tool_offset"):
                current_machine['tool_offset'] = [float(x.replace(',', '.')) for x in line.split()[1:]]
            elif line.startswith("velocity"):
                current_machine['velocity'] = float(line.split()[1].replace(',', '.'))

    if current_machine:
        machines.append(current_machine)

    return machines
    
def send_machine_data(machine):
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }

    data = {
        'name': machine['name'],
        'acceleration': machine['acceleration'],
        'actual_position': [machine['actual_position']],
        'distance_to_go': [machine['distance_to_go']],
        'homed': [machine['homed']],
        'tool_offset': [machine['tool_offset']],
        'velocity': machine['velocity'],
    }
    
    print(f"Sending data for machine {machine['name']}: {data}")
    print(api_url)
    response = requests.post(api_url, json=data,headers=headers)
    if response.status_code == 200:
        print(f"Data for {machine['name']} sent successfully.")
    elif(response.status_code == 201):
        print(f"Data is created for {machine['name']}")
    else:
        print(f"Failed to send data for {machine['name']}. Status Code: {response.status_code}, Response: {response.text}")


# Main function to parse the file and send the data
def main():
    while(True):
        machines = parse_cnc_file(file_path)
        for machine in machines:
            send_machine_data(machine)
        time.sleep(25)

# if __name__ == '__main__':
main()