class CustomError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class PermissionDeniedError(CustomError):
    def __init__(self, role):
        super().__init__(f"Permission denied. The user with role '{role}' is not authorized to perform this action.", 403)

class MachineNotFoundError(CustomError):
    def __init__(self, machine_name):
        super().__init__(f"Machine {machine_name} not found.", 404)

class InvalidDataError(CustomError):
    def __init__(self, message="Invalid data provided."):
        super().__init__(message, 400)
