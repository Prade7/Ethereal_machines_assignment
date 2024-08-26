from flask import Blueprint, request, jsonify
from application import db
from application.models import Machine, DynamicData, User
from datetime import datetime
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from application.errors import PermissionDeniedError, InvalidDataError, MachineNotFoundError
from werkzeug.security import check_password_hash

routes = Blueprint('routes', __name__)


@routes.route('/api/login', methods=['POST'])
def login():
    # Get employee ID and password from the request
    employee_id = request.json.get('employee_id', None)
    password = request.json.get('password', None)

    # Validate input
    if not employee_id or not password:
        raise InvalidDataError("Employee ID and password are required.")

    # Query the user by employee ID
    user = User.query.filter_by(employee_id=employee_id).first()

    if user:
        # Check if the password is correct
        if check_password_hash(user.password_hash, password):
            # Create JWT token
            access_token = create_access_token(
                identity={'employee_id': user.employee_id, 'role': user.role, 'user_id': user.id},
                expires_delta=False
            )
            return jsonify(access_token=access_token), 200
        else:
            # If password is incorrect
            return jsonify({"error": "Invalid password."}), 401
    else:
        # Create new user if not found
        new_user = User(employee_id=employee_id)
        new_user.set_password(password)
        new_user.role = request.json.get('role', 'Operator')  # Default role as 'Operator' if not provided
        db.session.add(new_user)
        db.session.commit()

        # Create JWT token for the new user
        access_token = create_access_token(
            identity={'employee_id': new_user.employee_id, 'role': new_user.role, 'user_id': new_user.id},
            expires_delta=False
        )
        return jsonify(access_token=access_token), 200














@routes.route('/machine', methods=['PUT','POST','GET','DELETE'])
@jwt_required()
def machine():
    current_user = get_jwt_identity()

    user_details = User.query.filter_by(employee_id=current_user['employee_id']).first()
    if not user_details:
        return jsonify(f"Your data is not found in the db MR - {current_user['employee_id']}"),404

    if request.method =="DELETE":
        employee_id = current_user["employee_id"]
        return jsonify(f"You cannot delete MR - {employee_id}"),404

    if request.method =="GET":
        machines = Machine.query.all()
    
        # Group data by machine name
        result = []
        for machine in machines:
            machine_data = {
                'name': machine.name,
                'acceleration': machine.acceleration,
                'velocity': machine.velocity,
                'dynamic_data': []
            }
            
            for dynamic_data in machine.dynamic_data:
                dynamic_data_entry = {
                    'actual_position': {
                        'x': dynamic_data.actual_position_x,
                        'y': dynamic_data.actual_position_y,
                        'z': dynamic_data.actual_position_z,
                        'a': dynamic_data.actual_position_a,
                        'c': dynamic_data.actual_position_c
                    },
                    'distance_to_go': {
                        'x': dynamic_data.distance_to_go_x,
                        'y': dynamic_data.distance_to_go_y,
                        'z': dynamic_data.distance_to_go_z,
                        'a': dynamic_data.distance_to_go_a,
                        'c': dynamic_data.distance_to_go_c
                    },
                    'homed': {
                        'x': dynamic_data.homed_x,
                        'y': dynamic_data.homed_y,
                        'z': dynamic_data.homed_z,
                        'a': dynamic_data.homed_a,
                        'c': dynamic_data.homed_c
                    },
                    'tool_offset': {
                        'x': dynamic_data.tool_offset_x,
                        'y': dynamic_data.tool_offset_y,
                        'z': dynamic_data.tool_offset_z,
                        'a': dynamic_data.tool_offset_a,
                        'c': dynamic_data.tool_offset_c
                    },
                    'created_by': dynamic_data.created_by,
                    'timestamp':dynamic_data.timestamp
                }
                machine_data['dynamic_data'].append(dynamic_data_entry)

            result.append(machine_data)

        return jsonify(result), 200




    data = request.get_json()
    if not data or 'name' not in data:
        raise InvalidDataError("Missing machine name in the data.")

    machine_name = data['name']
    

    if current_user["role"].lower()=='supervisor':
        machine = Machine.query.filter_by(name=machine_name).first()
        if not machine:
            raise PermissionDeniedError(current_user['role'])
    

    if current_user['role'].lower()=='operator':
        raise PermissionDeniedError(current_user['role'])
    machine = Machine.query.filter_by(name=machine_name, acceleration=data['acceleration'], velocity=data['velocity']).first()


    if machine:
        machine.acceleration = data['acceleration']
        machine.velocity = data['velocity']
        latest_dynamic_data = DynamicData.query.filter_by(
            machine_id=machine.id,
            actual_position_x=data['actual_position']['x'],
            actual_position_y=data['actual_position']['y'],
            actual_position_z=data['actual_position']['z'],
            actual_position_a=data['actual_position']['a'],
            actual_position_c=data['actual_position']['c'],
            distance_to_go_x=data['distance_to_go']['x'],
            distance_to_go_y=data['distance_to_go']['y'],
            distance_to_go_z=data['distance_to_go']['z'],
            distance_to_go_a=data['distance_to_go']['a'],
            distance_to_go_c=data['distance_to_go']['c'],
            homed_x=data['homed']['x'],
            homed_y=data['homed']['y'],
            homed_z=data['homed']['z'],
            homed_a=data['homed']['a'],
            homed_c=data['homed']['c'],
            tool_offset_x=data['tool_offset']['x'],
            tool_offset_y=data['tool_offset']['y'],
            tool_offset_z=data['tool_offset']['z'],
            tool_offset_a=data['tool_offset']['a'],
            tool_offset_c=data['tool_offset']['c']
        ).first()

        if not latest_dynamic_data:
            new_dynamic_data = DynamicData(
                machine_id=machine.id,
                user_id=current_user['user_id'],
                actual_position_x=data['actual_position']['x'],
                actual_position_y=data['actual_position']['y'],
                actual_position_z=data['actual_position']['z'],
                actual_position_a=data['actual_position']['a'],
                actual_position_c=data['actual_position']['c'],
                distance_to_go_x=data['distance_to_go']['x'],
                distance_to_go_y=data['distance_to_go']['y'],
                distance_to_go_z=data['distance_to_go']['z'],
                distance_to_go_a=data['distance_to_go']['a'],
                distance_to_go_c=data['distance_to_go']['c'],
                homed_x=data['homed']['x'],
                homed_y=data['homed']['y'],
                homed_z=data['homed']['z'],
                homed_a=data['homed']['a'],
                homed_c=data['homed']['c'],
                tool_offset_x=data['tool_offset']['x'],
                tool_offset_y=data['tool_offset']['y'],
                tool_offset_z=data['tool_offset']['z'],
                tool_offset_a=data['tool_offset']['a'],
                tool_offset_c=data['tool_offset']['c'],
                created_by=current_user["employee_id"],
                timestamp=datetime.now()
            )
            db.session.add(new_dynamic_data)
            db.session.commit()
    else:
        
        new_machine = Machine(
            name=machine_name,
            acceleration=data['acceleration'],
            velocity=data['velocity'],
            
        )
        db.session.add(new_machine)
        db.session.commit()

        new_dynamic_data = DynamicData(
            machine_id=new_machine.id,
            user_id=current_user['user_id'],
            actual_position_x=data['actual_position']['x'],
            actual_position_y=data['actual_position']['y'],
            actual_position_z=data['actual_position']['z'],
            actual_position_a=data['actual_position']['a'],
            actual_position_c=data['actual_position']['c'],
            distance_to_go_x=data['distance_to_go']['x'],
            distance_to_go_y=data['distance_to_go']['y'],
            distance_to_go_z=data['distance_to_go']['z'],
            distance_to_go_a=data['distance_to_go']['a'],
            distance_to_go_c=data['distance_to_go']['c'],
            homed_x=data['homed']['x'],
            homed_y=data['homed']['y'],
            homed_z=data['homed']['z'],
            homed_a=data['homed']['a'],
            homed_c=data['homed']['c'],
            tool_offset_x=data['tool_offset']['x'],
            tool_offset_y=data['tool_offset']['y'],
            tool_offset_z=data['tool_offset']['z'],
            tool_offset_a=data['tool_offset']['a'],
            tool_offset_c=data['tool_offset']['c'],
            created_by=current_user["employee_id"],
            timestamp=datetime.now()
        )
        db.session.add(new_dynamic_data)
        db.session.commit()
        
        return jsonify({"message": f"Machine {machine_name} created and data added."}), 201

    return jsonify({"message": f"Machine {machine_name} updated."}), 200


# @jwt_required()


@routes.route('/viewmachines', methods=['GET'])            #An route to check the details in the browser
def get_machines():
 
    machines = Machine.query.all()
    
    # Group data by machine name
    result = []
    for machine in machines:
        machine_data = {
            'name': machine.name,
            'acceleration': machine.acceleration,
            'velocity': machine.velocity,
            'dynamic_data': []
        }
        
        for dynamic_data in machine.dynamic_data:
            dynamic_data_entry = {
                'actual_position': {
                    'x': dynamic_data.actual_position_x,
                    'y': dynamic_data.actual_position_y,
                    'z': dynamic_data.actual_position_z,
                    'a': dynamic_data.actual_position_a,
                    'c': dynamic_data.actual_position_c
                },
                'distance_to_go': {
                    'x': dynamic_data.distance_to_go_x,
                    'y': dynamic_data.distance_to_go_y,
                    'z': dynamic_data.distance_to_go_z,
                    'a': dynamic_data.distance_to_go_a,
                    'c': dynamic_data.distance_to_go_c
                },
                'homed': {
                    'x': dynamic_data.homed_x,
                    'y': dynamic_data.homed_y,
                    'z': dynamic_data.homed_z,
                    'a': dynamic_data.homed_a,
                    'c': dynamic_data.homed_c
                },
                'tool_offset': {
                    'x': dynamic_data.tool_offset_x,
                    'y': dynamic_data.tool_offset_y,
                    'z': dynamic_data.tool_offset_z,
                    'a': dynamic_data.tool_offset_a,
                    'c': dynamic_data.tool_offset_c
                },
                'created_by': dynamic_data.created_by,
                'timestamp':dynamic_data.timestamp
            }
            machine_data['dynamic_data'].append(dynamic_data_entry)

        result.append(machine_data)

    return jsonify(result), 200






