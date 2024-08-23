from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from application import db
from application.models import Machine, DynamicData
from datetime import datetime
from application.errors import PermissionDeniedError, InvalidDataError, MachineNotFoundError

routes = Blueprint('routes', __name__)

USER_ROLES = {
    'manager': 'Manager',
    'supervisor': 'Supervisor',
    'operator': 'Operator'
}

def user_has_permission(user_role, method):
    permissions = {
        'Manager': {'POST': True, 'GET': True, 'PUT': True, 'DELETE': False},
        'Supervisor': {'POST': False, 'GET': True, 'PUT': True, 'DELETE': False},
        'Operator': {'POST': False, 'GET': True, 'PUT': False, 'DELETE': False},
    }
    return permissions.get(user_role, {}).get(method, False)

@routes.errorhandler(PermissionDeniedError)
def handle_permission_denied(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response

@routes.errorhandler(MachineNotFoundError)
def handle_machine_not_found(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response

@routes.errorhandler(InvalidDataError)
def handle_invalid_data(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response

@routes.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    role = USER_ROLES.get(username)
    
    if role:
        access_token = create_access_token(
            identity={'username': username, 'role': role},
            expires_delta=False
        )
        return jsonify(access_token=access_token), 200
    else:
        raise InvalidDataError("Invalid credentials")

@routes.route('/viewmachines', methods=['GET'])
def view_machines():
    # current_user = get_jwt_identity()
    # if not user_has_permission(current_user['role'], 'GET'):
    #     raise PermissionDeniedError(current_user['role'])

    machines = Machine.query.all()
    grouped_data = {}

    for machine in machines:
        dynamic_data_list = DynamicData.query.filter_by(machine_name=machine.name).all()
        grouped_data[machine.name] = {
            'acceleration': machine.acceleration,
            'velocity': machine.velocity,
            'latest_timestamp': machine.timestamp,
            'dynamic_data': []
        }

        for data in dynamic_data_list:
            grouped_data[machine.name]['dynamic_data'].append({
                'actual_position': data.actual_position,
                'distance_to_go': data.distance_to_go,
                'homed': data.homed,
                'tool_offset': data.tool_offset,
            })

    return jsonify(grouped_data), 200

@routes.route('/updatemachine', methods=['POST'])
@jwt_required()
def update_machine():
    current_user = get_jwt_identity()
    if not user_has_permission(current_user['role'], 'POST'):
        raise PermissionDeniedError(current_user['role'])

    data = request.get_json()
    if not data or 'name' not in data:
        raise InvalidDataError("Missing machine name in the data.")

    machine_name = data['name']

    try:
        actual_position = {axis: value for axis, value in zip(['x', 'y', 'z', 'a', 'c'], data['actual_position'][0])}
        distance_to_go = {axis: value for axis, value in zip(['x', 'y', 'z', 'a', 'c'], data['distance_to_go'][0])}
        homed = {axis: value for axis, value in zip(['x', 'y', 'z', 'a', 'c'], data['homed'][0])}
        tool_offset = {axis: value for axis, value in zip(['x', 'y', 'z', 'a', 'c'], data['tool_offset'][0])}
    except (KeyError, IndexError):
        raise InvalidDataError(f"Incorrect data format for machine parameters.")

    machine = Machine.query.filter_by(name=machine_name).first()

    if machine:
        latest_dynamic_data = DynamicData.query.filter_by(machine_name=machine_name).first()

        if latest_dynamic_data:
            if (latest_dynamic_data.actual_position != actual_position or 
                latest_dynamic_data.distance_to_go != distance_to_go or
                latest_dynamic_data.homed != homed or
                latest_dynamic_data.tool_offset != tool_offset or 
                machine.acceleration != data['acceleration'] or 
                machine.velocity != data['velocity']):
                
                latest_dynamic_data.actual_position = actual_position
                latest_dynamic_data.distance_to_go = distance_to_go
                latest_dynamic_data.homed = homed
                latest_dynamic_data.tool_offset = tool_offset
                machine.acceleration = data['acceleration']
                machine.velocity = data['velocity']
                machine.timestamp = datetime.now()
                db.session.commit()
                return jsonify({"message": f"Machine {machine_name} updated."}), 200
            else:
                return jsonify({"message": f"No changes detected for machine {machine_name}."}), 200
        else:
            new_dynamic_data = DynamicData(
                machine_name=machine_name,
                actual_position=actual_position,
                distance_to_go=distance_to_go,
                homed=homed,
                tool_offset=tool_offset,
            )
            db.session.add(new_dynamic_data)
            db.session.commit()
            return jsonify({"message": f"New dynamic data added for machine {machine_name}."}), 201
    else:
        new_machine = Machine(
            name=machine_name,
            acceleration=data['acceleration'],
            velocity=data['velocity'],
            timestamp=datetime.now()
        )
        new_dynamic_data = DynamicData(
            machine_name=machine_name,
            actual_position=actual_position,
            distance_to_go=distance_to_go,
            homed=homed,
            tool_offset=tool_offset,
        )
        db.session.add(new_machine)
        db.session.add(new_dynamic_data)
        db.session.commit()
        return jsonify({"message": f"Machine {machine_name} added to the database."}), 201

@routes.route('/deletemachine/<string:machine_name>', methods=['DELETE'])
@jwt_required()
def delete_machine(machine_name):
    current_user = get_jwt_identity()
    if not user_has_permission(current_user['role'], 'DELETE'):
        raise PermissionDeniedError(current_user['role'])

    machine = Machine.query.filter_by(name=machine_name).first()

    if machine: 
        DynamicData.query.filter_by(machine_name=machine_name).delete()
        db.session.delete(machine)
        db.session.commit()
        return jsonify({"message": f"Machine {machine_name} deleted."}), 200
    else:
        raise MachineNotFoundError(machine_name)
