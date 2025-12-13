from flask import Blueprint, request, jsonify
from models import Target, Campaign, PhishingResult, EmailTemplate
from sqlalchemy.exc import IntegrityError
from extensions import db

targets_bp = Blueprint('targets', __name__)

@targets_bp.route('/', methods=['POST'])
def create_target():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    new_target = Target(
        email=email,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        department=data.get('department')
    )
    
    try:
        db.session.add(new_target)
        db.session.commit()
        return jsonify({'message': 'Target created', 'id': new_target.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@targets_bp.route('/', methods=['GET'])
def list_targets():
    targets = Target.query.all()
    result = []
    for t in targets:
        # Fetch history
        history_records = PhishingResult.query.filter_by(target_id=t.id).all()
        history = []
        for h in history_records:
            campaign = Campaign.query.get(h.campaign_id)
            template = EmailTemplate.query.get(campaign.template_id) if campaign else None
            history.append({
                'result_id': h.id,
                'campaign_name': campaign.name if campaign else 'Unknown',
                'email_subject': template.subject if template else 'Unknown',
                'email_body': template.body_content if template else 'No content',
                'sent_at': h.sent_at.isoformat(),
                'status': 'Clicked' if h.clicked_link else 'Opened' if h.opened else 'Sent'
            })

        result.append({
            'id': t.id,
            'email': t.email,
            'first_name': t.first_name,
            'last_name': t.last_name,
            'department': t.department,
            'history': history
        })
    return jsonify(result)

@targets_bp.route('/<int:id>', methods=['DELETE'])
def delete_target(id):
    target = Target.query.get_or_404(id)
    db.session.delete(target)
    db.session.commit()
    return jsonify({'message': 'Target deleted'}), 200
