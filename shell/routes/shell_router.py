from flask import Blueprint, session, redirect

shell_bp = Blueprint('shell', __name__, url_prefix='/shell')

@shell_bp.route('/')
def entry():
    user = session.get('user')
    if not user:
        return redirect('/login')

    role = user.get('role')

    if role == 'DELIVERY':
        return redirect('/delivery')
    elif role == 'OFFICE':
        return redirect('/office')
    elif role == 'OWNER':
        return redirect('/owner')
    elif role == 'ACCOUNTS':
        return redirect('/accounts')

    return 'Unauthorized role', 403
