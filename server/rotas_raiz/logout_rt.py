# server/rotas_raiz/logout_rt.py
from flask import Blueprint, redirect, url_for, session, flash
# Removed unused imports: render_template, request, verify_user, generate_auth_token
# login_required is a decorator, not directly called here.

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('jwt_token', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login.login')) # Explicitly use blueprint.route_name