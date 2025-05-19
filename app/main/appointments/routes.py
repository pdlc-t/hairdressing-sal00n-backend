import random
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from flask import request, jsonify, current_app

from app.extensions import db
from app.main.appointments import bp
from app.main.models.appointment import Appointment
from app.main.models.hairdresser import Hairdresser


@bp.route('/get-appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments])

@bp.route('/add-appointment', methods=['POST'])
def add_appointment():
    data = request.get_json()

    if not data or not all(k in data for k in ("service_id", "date", "time_slot")):
        return jsonify({'error': 'Missing required fields'}), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization token'}), 401

    token = auth_header.split(' ')[1]
    try:
        decoded_token = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        client_id = decoded_token['user_id']
    except InvalidTokenError:
        return jsonify({'error': 'Invalid or expired token'}), 401

    # losowy fryzjer z puli
    hairdressers = Hairdresser.query.all()
    if not hairdressers:
        return jsonify({'error': 'No hairdressers available'}), 500
    chosen_hairdresser = random.choice(hairdressers)

    try:
        new_appointment = Appointment(
            client_id=client_id,
            service_id=data['service_id'],
            hairdresser_id=chosen_hairdresser.id,        # przypisanie fryzjera
            date=datetime.fromisoformat(data['date']),
            time_slot=data['time_slot']
        )
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({
            'message': 'Appointment added successfully',
            'appointment': new_appointment.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to add the appointment',
            'details': str(e)
        }), 500

@bp.route('/get-busy-time-slots', methods=['GET'])
def get_busy_time_slots():
    date_string = request.args.get('date')
    print(f'Date string {date_string}')

    if not date_string:
        return jsonify({'error': 'Missing date parameter'}), 400

    try:
        target_date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        next_day = target_date + timedelta(days=1)
        # date_only = parsed_date.date()
        print(f'Date string parsed: {target_date}')

        appointments = Appointment.query.filter(
            Appointment.date >= target_date,
            Appointment.date < next_day
        ).all()

        timeslots = { 1: True, 2: True, 3: True, 4: True, 5: True }

        for appointment in appointments:
            timeslots[appointment.time_slot] = False

        return jsonify(timeslots), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization token'}), 401

    token = auth_header.split(' ')[1]
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        client_id = decoded['user_id']
    except InvalidTokenError:
        return jsonify({'error': 'Invalid or expired token'}), 401

    appt = Appointment.query.get(appointment_id)
    if not appt:
        return jsonify({'error': 'Appointment not found'}), 404
    if appt.client_id != client_id:
        return jsonify({'error': 'Not allowed to cancel this appointment'}), 403

    try:
        db.session.delete(appt)
        db.session.commit()
        return jsonify({'message': 'Appointment cancelled'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel', 'details': str(e)}), 500
