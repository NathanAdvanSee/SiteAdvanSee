# assets.py

from flask import Blueprint, request, jsonify
# REMOVIDO: from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Asset, AssetCategory, Vendor, Location, Organization # REMOVIDO: User
from datetime import datetime
# REMOVIDO: import bcrypt # Não é mais necessário

assets_bp = Blueprint('assets', __name__)

# REMOVIDO: Função auxiliar para validar credenciais

@assets_bp.route('/', methods=['GET'])
def get_assets():
    try:
        # Usar a primeira organização padrão para filtrar dados
        organization = Organization.query.first() 
        if not organization:
            return jsonify({'error': 'No organization found'}), 500
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status', '')
        
        query = Asset.query.filter_by(organization_id=organization.id)
        
        if search:
            query = query.filter(
                db.or_(
                    Asset.name.ilike(f'%{search}%'),
                    Asset.asset_tag.ilike(f'%{search}%'),
                    Asset.serial_number.ilike(f'%{search}%')
                )
            )
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if status:
            query = query.filter_by(status=status)
        
        assets = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'assets': [{
                'id': asset.id,
                'asset_tag': asset.asset_tag,
                'name': asset.name,
                'description': asset.description,
                'category': asset.category.name if asset.category else None,
                'vendor': asset.vendor.name if asset.vendor else None,
                'model': asset.model,
                'serial_number': asset.serial_number,
                'status': asset.status,
                'criticality': asset.criticality,
                'ip_address': asset.ip_address,
                'operating_system': asset.operating_system,
                'location': asset.location.name if asset.location else None,
                'assigned_user': f"{asset.assigned_user.first_name} {asset.assigned_user.last_name}" if asset.assigned_user else None, # asset.assigned_user pode ser None aqui se o user não for importado
                'last_seen': asset.last_seen.isoformat() if asset.last_seen else None,
                'created_at': asset.created_at.isoformat()
            } for asset in assets.items],
            'pagination': {
                'page': assets.page,
                'pages': assets.pages,
                'per_page': assets.per_page,
                'total': assets.total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    try:
        # Como não há autenticação de usuário, a busca é por ID global
        asset = Asset.query.filter_by(id=asset_id).first()
        
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        return jsonify({
            'id': asset.id,
            'asset_tag': asset.asset_tag,
            'name': asset.name,
            'description': asset.description,
            'category_id': asset.category_id,
            'category': asset.category.name if asset.category else None,
            'vendor_id': asset.vendor_id,
            'vendor': asset.vendor.name if asset.vendor else None,
            'model': asset.model,
            'serial_number': asset.serial_number,
            'purchase_date': asset.purchase_date.isoformat() if asset.purchase_date else None,
            'purchase_cost': float(asset.purchase_cost) if asset.purchase_cost else None,
            'warranty_expiry': asset.warranty_expiry.isoformat() if asset.warranty_expiry else None,
            'location_id': asset.location_id,
            'location': asset.location.name if asset.location else None,
            'assigned_user_id': asset.assigned_user_id,
            'assigned_user': None, # Não há user logado para mostrar o nome completo
            'status': asset.status,
            'criticality': asset.criticality,
            'ip_address': asset.ip_address,
            'mac_address': asset.mac_address,
            'operating_system': asset.operating_system,
            'os_version': asset.os_version,
            'last_seen': asset.last_seen.isoformat() if asset.last_seen else None,
            'created_at': asset.created_at.isoformat(),
            'updated_at': asset.updated_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# REMOVIDO: @assets_bp.route('/', methods=['POST']) def create_asset(): ...
# REMOVIDO: @assets_bp.route('/<int:asset_id>', methods=['PUT']) def update_asset(asset_id): ...
# REMOVIDO: @assets_bp.route('/<int:asset_id>', methods=['DELETE']) def delete_asset(asset_id): ...

@assets_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = AssetCategory.query.all()
        
        return jsonify([{
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'parent_id': category.parent_id
        } for category in categories]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/vendors', methods=['GET'])
def get_vendors():
    try:
        vendors = Vendor.query.all()
        
        return jsonify([{
            'id': vendor.id,
            'name': vendor.name,
            'contact_email': vendor.contact_email,
            'contact_phone': vendor.contact_phone
        } for vendor in vendors]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/locations', methods=['GET'])
def get_locations():
    try:
        # Usar a primeira organização padrão
        organization = Organization.query.first() 
        if not organization:
            return jsonify({'error': 'No organization found'}), 500

        locations = Location.query.filter_by(organization_id=organization.id).all()
        
        return jsonify([{
            'id': location.id,
            'name': location.name,
            'address': location.address,
            'building': location.building,
            'floor': location.floor,
            'room': location.room
        } for location in locations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500