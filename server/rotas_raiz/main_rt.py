# server/rotas_raiz/main_rt.py
from flask import Blueprint, render_template, request, session, current_app
from server.rotas_raiz.rotas_autenticar.auth_rt import login_required
from server.Database.modelo_base_dados import db, Asset, AssetCategory, User, Location
import json # For graph data

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Fetch data for dashboard
    total_assets = Asset.query.count()
    assets_online = Asset.query.filter_by(status='active').count()
    assets_maintenance = Asset.query.filter_by(status='maintenance').count()
    assets_offline = Asset.query.filter_by(status='decommissioned').count()

    # Data for charts (dummy data for now, replace with real database queries)
    # Assets by Category
    category_counts = db.session.query(AssetCategory.name, db.func.count(Asset.id))\
                              .outerjoin(Asset)\
                              .group_by(AssetCategory.name)\
                              .all()
    categories_names = [name for name, _ in category_counts]
    categories_values = [count for _, count in category_counts]

    graph_category_data = {
        'data': [
            {
                'labels': categories_names,
                'values': categories_values,
                'type': 'pie',
                'name': 'Assets by Category'
            }
        ],
        'layout': {
            'title': 'Equipamentos por Categoria',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white'}
        }
    }
    graph_category_json = json.dumps(graph_category_data)

    # Assets by Status
    status_counts = db.session.query(Asset.status, db.func.count(Asset.id))\
                            .group_by(Asset.status)\
                            .all()
    status_names = [status for status, _ in status_counts]
    status_values = [count for _, count in status_counts]

    graph_status_data = {
        'data': [
            {
                'x': status_names,
                'y': status_values,
                'type': 'bar',
                'marker': {'color': ['#22c55e', '#f59e0b', '#ef4444']} # Colors for active, maintenance, decommissioned
            }
        ],
        'layout': {
            'title': 'Equipamentos por Status',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white'}
        }
    }
    graph_status_json = json.dumps(graph_status_data)

    user_role = session.get('user_role', 'user') # Get user role from session

    return render_template('dasboard.html',
                           total_assets=total_assets,
                           assets_online=assets_online,
                           assets_maintenance=assets_maintenance,
                           assets_offline=assets_offline,
                           user_role=user_role,
                           graph_category_json=graph_category_json,
                           graph_status_json=graph_status_json)

@main_bp.route('/equipamentos')
@login_required
def equipamentos_list():
    search_query = request.args.get('search_query', '')
    category_id = request.args.get('category', 'all')
    status = request.args.get('status', 'all')

    assets_query = Asset.query.join(User, Asset.assigned_user_id == User.id, isouter=True) \
                             .join(AssetCategory, Asset.category_id == AssetCategory.id, isouter=True) \
                             .join(Location, Asset.location_id == Location.id, isouter=True)

    if search_query:
        assets_query = assets_query.filter(
            (Asset.name.ilike(f'%{search_query}%')) |
            (Asset.asset_tag.ilike(f'%{search_query}%')) |
            (Asset.serial_number.ilike(f'%{search_query}%')) |
            (User.username.ilike(f'%{search_query}%'))
        )

    if category_id != 'all':
        assets_query = assets_query.filter(Asset.category_id == int(category_id))

    if status != 'all':
        assets_query = assets_query.filter(Asset.status == status)

    assets = assets_query.all()
    categories = AssetCategory.query.all() # Fetch all categories for the filter dropdown

    return render_template('equipamentos_lista.html', assets=assets, categories=categories)