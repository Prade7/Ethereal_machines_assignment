from flask import jsonify

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

class PermissionDeniedError(Exception):
    def __init__(self, role):
        self.message = f"Permission denied for role: {role}"

class MachineNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

# Error handler for InvalidDataError
def handle_invalid_data_error(error):
    response = jsonify({"error": error.message})
    response.status_code = 400  # Bad Request
    return response

# Error handler for PermissionDeniedError
def handle_permission_denied_error(error):
    response = jsonify({"error": error.message})
    response.status_code = 403  # Forbidden
    return response

# Error handler for MachineNotFoundError
def handle_machine_not_found_error(error):
    response = jsonify({"error": error.message})
    response.status_code = 404  # Not Found
    return response

# Function to register error handlers with Flask app
def register_error_handlers(app):
    app.register_error_handler(InvalidDataError, handle_invalid_data_error)
    app.register_error_handler(PermissionDeniedError, handle_permission_denied_error)
    app.register_error_handler(MachineNotFoundError, handle_machine_not_found_error)
