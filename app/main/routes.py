from app.main import bp

@bp.route('/')
def hello():
    return '<h1>Siema siema o tej porze, każdy wypić może</h1>'