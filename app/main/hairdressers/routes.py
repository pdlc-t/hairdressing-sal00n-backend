from flask import request, jsonify, abort
from app.auth import require_auth
from app.main.hairdressers import bp
from app.extensions import db
from app.main.models.hairdresser import Hairdresser
from app.main.models.comment import Comment
import json

@bp.route('/', methods=['GET'])
@require_auth
def hairdresser_list():
    hairdressers = Hairdresser.query.all()
    result = []
    for hd in hairdressers:
        # build list of comments manually
        comments = []
        for c in hd.comments:
            comments.append({
                "id": c.id,
                "author": c.author,
                "content": c.content,
                "created_at": c.created_at.isoformat()
            })
        result.append({
            "id": hd.id,
            "firstName": hd.firstName,
            "lastName": hd.lastName,
            "specialties": json.loads(hd.specialties),
            "rating": hd.rating,
            "comments": comments
        })
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
@require_auth
def get_hairdresser(id):
    hd = Hairdresser.query.get_or_404(id)
    comments = [{
        "id": c.id,
        "author": c.author,
        "content": c.content,
        "created_at": c.created_at.isoformat()
    } for c in hd.comments]
    return jsonify({
        "id": hd.id,
        "firstName": hd.firstName,
        "lastName": hd.lastName,
        "specialties": json.loads(hd.specialties),
        "rating": hd.rating,
        "comments": comments
    }), 200

@bp.route('/', methods=['POST'])
@require_auth
def create_hairdresser():
    data = request.get_json() or {}
    required = ['firstName', 'lastName', 'specialties', 'rating']
    if not all(field in data for field in required):
        abort(400, description="Missing fields")
    hd = Hairdresser(
        firstName   = data['firstName'],
        lastName    = data['lastName'],
        specialties = json.dumps(data['specialties']),
        rating      = data['rating']
    )
    db.session.add(hd)
    db.session.commit()
    return jsonify({
        "id": hd.id,
        "firstName": hd.firstName,
        "lastName": hd.lastName,
        "specialties": data['specialties'],
        "rating": hd.rating,
        "comments": []
    }), 201

@bp.route('/<int:id>', methods=['PUT'])
@require_auth
def update_hairdresser(id):
    hd = Hairdresser.query.get_or_404(id)
    data = request.get_json() or {}
    if 'firstName' in data:
        hd.firstName = data['firstName']
    if 'lastName' in data:
        hd.lastName = data['lastName']
    if 'specialties' in data:
        hd.specialties = json.dumps(data['specialties'])
    if 'rating' in data:
        hd.rating = data['rating']
    db.session.commit()
    comments = [{
        "id": c.id,
        "author": c.author,
        "content": c.content,
        "created_at": c.created_at.isoformat()
    } for c in hd.comments]
    return jsonify({
        "id": hd.id,
        "firstName": hd.firstName,
        "lastName": hd.lastName,
        "specialties": json.loads(hd.specialties),
        "rating": hd.rating,
        "comments": comments
    }), 200

@bp.route('/<int:id>', methods=['DELETE'])
@require_auth
def delete_hairdresser(id):
    hd = Hairdresser.query.get_or_404(id)
    db.session.delete(hd)
    db.session.commit()
    return jsonify({
        "message": "Deleted",
        "id": id
    }), 200

# Comment endpoints:

@bp.route('/<int:hd_id>/comments', methods=['GET'])
@require_auth
def list_comments(hd_id):
    hairdresser = Hairdresser.query.get_or_404(hd_id)
    comments = []
    for c in hairdresser.comments:
        comments.append({
            "id": c.id,
            "author": c.author,
            "content": c.content,
            "created_at": c.created_at.isoformat()
        })
    return jsonify(comments), 200

@bp.route('/<int:hd_id>/comments', methods=['POST'])
@require_auth
def create_comment(hd_id):
    Hairdresser.query.get_or_404(hd_id)
    data = request.get_json() or {}
    if 'content' not in data:
        abort(400, description="Missing comment content")
    comment = Comment(
        hairdresser_id=hd_id,
        author=data.get('author'),
        content=data['content']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        "id": comment.id,
        "author": comment.author,
        "content": comment.content,
        "created_at": comment.created_at.isoformat()
    }), 201

@bp.route('/<int:hd_id>/comments/<int:c_id>', methods=['PUT'])
@require_auth
def update_comment(hd_id, c_id):
    comment = Comment.query.filter_by(id=c_id, hairdresser_id=hd_id).first_or_404()
    data = request.get_json() or {}
    if 'content' in data:
        comment.content = data['content']
    if 'author' in data:
        comment.author = data['author']
    db.session.commit()
    return jsonify({
        "id": comment.id,
        "author": comment.author,
        "content": comment.content,
        "created_at": comment.created_at.isoformat()
    }), 200

@bp.route('/<int:hd_id>/comments/<int:c_id>', methods=['DELETE'])
@require_auth
def delete_comment(hd_id, c_id):
    comment = Comment.query.filter_by(id=c_id, hairdresser_id=hd_id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({
        "message": "Comment deleted",
        "id": c_id
    }), 200
