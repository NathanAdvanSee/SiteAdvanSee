# agents.py

from flask import Blueprint, request, jsonify
# REMOVIDO: from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Asset, Agent, Organization, AssetHistory # REMOVIDO: User
from datetime import datetime, timedelta
# REMOVIDO: import bcrypt # Não é mais necessário

agents_bp = Blueprint('agents', __name__)

# REMOVIDO: Função auxiliar para validar credenciais

@agents_bp.route('/', methods=['GET'])
def get_agents():
    try:
        # Usar a primeira organização padrão
        organization = Organization.query.first() 
        if not organization:
            return jsonify({'error': 'No organization found'}), 500

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', '')
        
        query = db.session.query(Agent, Asset).join(
            Asset, Agent.asset_id == Asset.id # <--- CORRIGIDO AQUI
        ).filter(Asset.organization_id == organization.id)
        
        if status:
            query = query.filter(Agent.status == status)
        
        agents = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'agents': [{
                'id': agent.id,
                'asset_id': asset.id,
                'asset_name': asset.name,
                'asset_tag': asset.asset_tag,
                'agent_version': agent.agent_version,
                'status': agent.status,
                'last_checkin': agent.last_checkin.isoformat() if agent.last_checkin else None,
                'created_at': agent.created_at.isoformat(),
                'is_online': (datetime.utcnow() - agent.last_checkin).total_seconds() < 300 if agent.last_checkin else False
            } for agent, asset in agents.items],
            'pagination': {
                'page': agents.page,
                'pages': agents.pages,
                'per_page': agents.per_page,
                'total': agents.total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/checkin', methods=['POST'])
def agent_checkin():
    # Esta rota não precisa de autenticação para o agente (já era pública)
    try:
        data = request.get_json()
        asset_tag = data.get('asset_tag')
        agent_version = data.get('agent_version')
        system_info = data.get('system_info', {})
        
        if not asset_tag:
            return jsonify({'error': 'Asset tag is required'}), 400
        
        organization = Organization.query.first() # Usar a primeira organização padrão
        if not organization:
            return jsonify({'error': 'No organization found to assign asset'}), 500
        organization_id = organization.id

        asset = Asset.query.filter_by(asset_tag=asset_tag, organization_id=organization_id).first()
        newly_created_asset = False
        
        if not asset:
            asset = Asset(
                organization_id=organization_id,
                asset_tag=asset_tag,
                name=system_info.get('hostname', f'Asset-{asset_tag[:8]}'),
                description='Discovered by agent check-in',
                status='active',
                criticality='medium',
                ip_address=system_info.get('ip_address'),
                mac_address=system_info.get('mac_address'),
                operating_system=system_info.get('operating_system'),
                os_version=system_info.get('os_version'),
                last_seen=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            db.session.add(asset)
            db.session.flush()
            newly_created_asset = True

            # user_id aqui seria None ou um ID de "sistema"
            history = AssetHistory(
                asset_id=asset.id,
                user_id=None, 
                action='created by agent',
                new_value=f'Asset automatically created by agent with tag {asset_tag}'
            )
            db.session.add(history)

        agent = Agent.query.filter_by(asset_id=asset.id).first()
        
        if not agent:
            agent = Agent(
                asset_id=asset.id,
                agent_version=agent_version,
                status='active'
            )
            db.session.add(agent)
        else:
            agent.agent_version = agent_version
            agent.status = 'active'
        
        agent.last_checkin = datetime.utcnow()
        agent.configuration = system_info
        agent.updated_at = datetime.utcnow()
        
        if system_info:
            updated_fields = []
            if 'ip_address' in system_info and asset.ip_address != system_info['ip_address']:
                updated_fields.append({'field': 'ip_address', 'old_value': asset.ip_address, 'new_value': system_info['ip_address']})
                asset.ip_address = system_info['ip_address']
            if 'operating_system' in system_info and asset.operating_system != system_info['operating_system']:
                updated_fields.append({'field': 'operating_system', 'old_value': asset.operating_system, 'new_value': system_info['operating_system']})
                asset.operating_system = system_info['operating_system']
            if 'os_version' in system_info and asset.os_version != system_info['os_version']:
                updated_fields.append({'field': 'os_version', 'old_value': asset.os_version, 'new_value': system_info['os_version']})
                asset.os_version = system_info['os_version']
            if 'mac_address' in system_info and asset.mac_address != system_info['mac_address']:
                updated_fields.append({'field': 'mac_address', 'old_value': asset.mac_address, 'new_value': system_info['mac_address']})
                asset.mac_address = system_info['mac_address']
            if 'hostname' in system_info and asset.name != system_info['hostname'] and not newly_created_asset:
                updated_fields.append({'field': 'name', 'old_value': asset.name, 'new_value': system_info['hostname']})
                asset.name = system_info['hostname']

            asset.last_seen = datetime.utcnow()
            asset.updated_at = datetime.utcnow()

            for change in updated_fields:
                history = AssetHistory(
                    asset_id=asset.id,
                    user_id=None, # user_id é None aqui
                    action='updated by agent',
                    field_name=change['field'],
                    old_value=str(change['old_value']),
                    new_value=str(change['new_value'])
                )
                db.session.add(history)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in successful',
            'agent_id': agent.id,
            'commands': []
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# REMOVIDO: @agents_bp.route('/<int:agent_id>/commands', methods=['POST']) def send_command_to_agent(agent_id): ...
@agents_bp.route('/stats', methods=['GET'])
def get_agent_stats():
    try:
        organization = Organization.query.first() 
        if not organization:
            return jsonify({'error': 'No organization found'}), 500
        
        total_agents = db.session.query(Agent).join(
            Asset, Agent.asset_id == Asset.id # <--- CORRIGIDO AQUI
        ).filter(Asset.organization_id == organization.id).count()
        
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        online_agents = db.session.query(Agent).join(
            Asset, Agent.asset_id == Asset.id # <--- CORRIGIDO AQUI
        ).filter(
            Asset.organization_id == organization.id,
            Agent.last_checkin >= five_minutes_ago
        ).count()
        
        offline_agents = total_agents - online_agents
        
        version_stats = db.session.query(
            Agent.agent_version,
            db.func.count(Agent.id).label('count')
        ).join(
            Asset, Agent.asset_id == Asset.id # <--- CORRIGIDO AQUI
        ).filter(
            Asset.organization_id == organization.id
        ).group_by(Agent.agent_version).all()
        
        return jsonify({
            'total_agents': total_agents,
            'online_agents': online_agents,
            'offline_agents': offline_agents,
            'by_version': {stat.agent_version or 'Unknown': stat.count for stat in version_stats}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# REMOVIDO: @agents_bp.route('/deploy', methods=['POST']) def deploy_agent(): ...