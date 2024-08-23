from application import db

class Machine(db.Model):
    __tablename__ = 'machines'
    name = db.Column(db.String, primary_key=True)
    acceleration = db.Column(db.Float, nullable=False)
    velocity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    dynamic_data = db.relationship('DynamicData', backref='machine', lazy=True)

class DynamicData(db.Model):
    __tablename__ = 'dynamic_data'
    id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String, db.ForeignKey('machines.name'), nullable=False)
    actual_position = db.Column(db.JSON, nullable=False)
    distance_to_go = db.Column(db.JSON, nullable=False)
    homed = db.Column(db.JSON, nullable=False)
    tool_offset = db.Column(db.JSON, nullable=False)

