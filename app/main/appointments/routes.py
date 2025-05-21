import random
from datetime import datetime, timedelta
from statistics import mean

import jwt
from jwt.exceptions import InvalidTokenError
from flask import request, jsonify, current_app

from app.extensions import db
from app.main.appointments import bp
from app.main.models.appointment import Appointment
from app.main.models.hairdresser import Hairdresser


@bp.route('/get-appointments', methods=['GET'])
def get_appointments():
    """
    Zwraca wszystkie umówione wizyty.
    Każda wizyta w słowniku zawiera:
      - id, client, service_name, price,
      - hairdresser { id, firstName, lastName },
      - date (ISO), time_slot
    """
    appointments = Appointment.query.all()
    return jsonify([appt.to_dict() for appt in appointments]), 200


@bp.route('/add-appointment', methods=['POST'])
def add_appointment():
    """
    Tworzy nową wizytę:
      - odczytuje JWT z nagłówka Authorization
      - dekoduje client_id
      - losowo wybiera fryzjera z bazy
      - zapisuje appointment
      - zwraca appointment.to_dict()
    """
    data = request.get_json() or {}
    if not all(k in data for k in ("service_id", "date", "time_slot")):
        return jsonify({'error': 'Missing required fields'}), 400

    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization token'}), 401

    token = auth_header.split(' ', 1)[1]
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        client_id = decoded.get('user_id')
    except InvalidTokenError:
        return jsonify({'error': 'Invalid or expired token'}), 401

    # Losowy fryzjer
    hairdressers = Hairdresser.query.all()
    if not hairdressers:
        return jsonify({'error': 'No hairdressers available'}), 500
    chosen_hd = random.choice(hairdressers)

    try:
        appt = Appointment(
            client_id=client_id,
            service_id=data['service_id'],
            hairdresser_id=chosen_hd.id,
            date=datetime.fromisoformat(data['date']),
            time_slot=data['time_slot']
        )
        db.session.add(appt)
        db.session.commit()

        return jsonify({
            'message': 'Appointment added successfully',
            'appointment': appt.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to add the appointment',
            'details': str(e)
        }), 500


@bp.route('/get-busy-time-slots', methods=['GET'])
def get_busy_time_slots():
    """
    Dla podanej daty (ISO w parametrach ?date=...) zwraca obiekt:
      {1: True|False, ..., 5: True|False}
    gdzie False znaczy, że slot jest zajęty.
    """
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Missing date parameter'}), 400

    try:
        start = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        end = start + timedelta(days=1)
        appts = Appointment.query.filter(
            Appointment.date >= start,
            Appointment.date < end
        ).all()

        slots = {i: True for i in range(1, 6)}
        for a in appts:
            slots[a.time_slot] = False

        return jsonify(slots), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """
    Usuwa wizytę:
      - weryfikuje JWT + client_id
      - sprawdza właściciela wizyty
      - usuwa i commit
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization token'}), 401

    token = auth_header.split(' ', 1)[1]
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        client_id = decoded.get('user_id')
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

@bp.route('/<int:appointment_id>/rate', methods=['POST'])
def rate_appointment(appointment_id):
    """
    Wystawia ocenę dla konkretnej wizyty, zapisuje ją w Appointment.rating,
    a następnie przelicza i aktualizuje hairdresser.rating jako średnią ze wszystkich ocen.
    """
    data = request.get_json() or {}
    if 'rating' not in data:
        return jsonify({'error': 'Missing rating field'}), 400

    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization token'}), 401
    token = auth_header.split(' ', 1)[1]

    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        client_id = decoded.get('user_id')
    except InvalidTokenError:
        return jsonify({'error': 'Invalid or expired token'}), 401

    appt = Appointment.query.get(appointment_id)
    if not appt:
        return jsonify({'error': 'Appointment not found'}), 404

    try:
        new_rating = int(data['rating'])
        if not (1 <= new_rating <= 5):
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({'error': 'Rating must be integer 1–5'}), 400

    # Zapisz ocenę w samej wizycie
    appt.rating = new_rating
    db.session.add(appt)

    # Przelicz średnią dla fryzjera
    all_ratings = [
        a.rating for a in Appointment.query
                                  .filter_by(hairdresser_id=appt.hairdresser_id)
                                  .filter(Appointment.rating.isnot(None))
                                  .all()
    ]
    avg = mean(all_ratings) if all_ratings else None

    # Zaktualizuj pole rating fryzjera
    hd = appt.hairdresser
    hd.rating = int(round(avg)) if avg is not None else None
    db.session.add(hd)

    db.session.commit()

    return jsonify({
        'message': 'Rated successfully',
        'appointment_rating': appt.rating,
        'hairdresser_avg_rating': hd.rating
    }), 200
@bp.route('get-clients-appointments')
def get_clients_appointments():
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

    clients_appointments = Appointment.query.filter(Appointment.client_id == client_id).all()
    return jsonify([appointment.to_dict() for appointment in clients_appointments])
