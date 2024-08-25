from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///machines.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'fjweFIUEFHUEFHEJFH'

db = SQLAlchemy(app)
jwt = JWTManager(app)




from flask import jsonify
from application.errors import PermissionDeniedError, InvalidDataError, MachineNotFoundError


@app.errorhandler(PermissionDeniedError)
def handle_permission_denied_error(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(InvalidDataError)
def handle_invalid_data_error(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(MachineNotFoundError)
def handle_machine_not_found_error(e):
    return jsonify(error=str(e)), 404
