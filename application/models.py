from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    acceleration = db.Column(db.Float, nullable=False)
    velocity = db.Column(db.Float, nullable=False)
    # created_by = db.Column(db.String(50), nullable=False)  # Tracks who created the record
    dynamic_data = db.relationship('DynamicData', backref='machine', lazy=True)

class DynamicData(db.Model):
    __tablename__ = 'dynamic_data'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    actual_position_x = db.Column(db.Float, nullable=False)
    actual_position_y = db.Column(db.Float, nullable=False)
    actual_position_z = db.Column(db.Float, nullable=False)
    actual_position_a = db.Column(db.Float, nullable=False)
    actual_position_c = db.Column(db.Float, nullable=False)
    distance_to_go_x = db.Column(db.Float, nullable=False)
    distance_to_go_y = db.Column(db.Float, nullable=False)
    distance_to_go_z = db.Column(db.Float, nullable=False)
    distance_to_go_a = db.Column(db.Float, nullable=False)
    distance_to_go_c = db.Column(db.Float, nullable=False)
    homed_x = db.Column(db.Boolean, nullable=False)
    homed_y = db.Column(db.Boolean, nullable=False)
    homed_z = db.Column(db.Boolean, nullable=False)
    homed_a = db.Column(db.Boolean, nullable=False)
    homed_c = db.Column(db.Boolean, nullable=False)
    tool_offset_x = db.Column(db.Float, nullable=False)
    tool_offset_y = db.Column(db.Float, nullable=False)
    tool_offset_z = db.Column(db.Float, nullable=False)
    tool_offset_a = db.Column(db.Float, nullable=False)
    tool_offset_c = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)  # Tracks who created the record
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
