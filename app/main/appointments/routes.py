from flask import request, jsonify, session

from app.extensions import db
from app.main.appointments import bp
from app.main.models.appointment import Appointment

@bp.route('/get-appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments])

@bp.route('/add-appointment', methods=['POST'])
def add_appointment():
    data = request.get_json()

    if not data or not all(k in data for k in ("client_id", "service_id", "date")):
        return jsonify({'error': 'Missing required fields'}), 400

    client_id = session.get('id')
    if not client_id:
        return jsonify({'error': 'Missing client_id - client not logged in ?...?'}), 400

    try:
        new_appointment = Appointment(
            client_id = session["id"],
            service_id = data['service_id'],
            date = data['date']
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment added successfully', 'appointment': new_appointment.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add the appointment', 'details': str(e)}), 500