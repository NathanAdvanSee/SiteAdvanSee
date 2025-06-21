from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from server.rotas_raiz.rotas_autenticar.auth_rt import login_required, verify_user, generate_auth_token

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('jwt_token', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))
