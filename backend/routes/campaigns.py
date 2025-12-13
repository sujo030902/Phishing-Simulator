from flask import Blueprint, request, jsonify
from models import Campaign, PhishingResult, Target
from extensions import db
from datetime import datetime

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/', methods=['POST'])
def create_campaign():
    data = request.get_json()
    name = data.get('name')
    template_id = data.get('template_id')
    
    if not name or not template_id:
        return jsonify({'error': 'Name and Template ID are required'}), 400
        
    new_campaign = Campaign(
        name=name,
        template_id=template_id,
        status='draft'
    )
    db.session.add(new_campaign)
    db.session.commit()
    
    return jsonify({'message': 'Campaign created', 'id': new_campaign.id}), 201

@campaigns_bp.route('/', methods=['GET'])
def list_campaigns():
    campaigns = Campaign.query.all()
    result = []
    for c in campaigns:
        result.append({
            'id': c.id,
            'name': c.name,
            'status': c.status,
            'created_at': c.created_at.isoformat(),
            'template_id': c.template_id
        })
    return jsonify(result)

@campaigns_bp.route('/<int:id>/launch', methods=['POST'])
def launch_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    if campaign.status != 'draft':
        return jsonify({'error': 'Campaign already active or completed'}), 400
        
    campaign.status = 'active'
    
    # Get selected targets from request
    data = request.get_json() or {}
    target_ids = data.get('target_ids')
    
    if target_ids:
        targets = Target.query.filter(Target.id.in_(target_ids)).all()
    else:
        # Fallback to all if no specific list provided (legacy behavior)
        targets = Target.query.all()
        
    for target in targets:
        result = PhishingResult(
            campaign_id=campaign.id,
            target_id=target.id,
            sent_at=datetime.utcnow()
        )
        db.session.add(result)
        
    db.session.commit()
    return jsonify({'message': f'Campaign {campaign.name} launched successfully. Emails sent to {len(targets)} targets.'}), 200

@campaigns_bp.route('/<int:id>/stats', methods=['GET'])
def campaign_stats(id):
    campaign = Campaign.query.get_or_404(id)
    results = PhishingResult.query.filter_by(campaign_id=id).all()
    
    total = len(results)
    opened = sum(1 for r in results if r.opened)
    clicked = sum(1 for r in results if r.clicked_link)
    submitted = sum(1 for r in results if r.submitted_credentials)
    
    return jsonify({
        'campaign': campaign.name,
        'status': campaign.status,
        'total_sent': total,
        'opened': opened,
        'clicked': clicked,
        'submitted': submitted
    })

@campaigns_bp.route('/<int:id>', methods=['DELETE'])
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    
    # Delete associated results first
    PhishingResult.query.filter_by(campaign_id=id).delete()
    
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted'}), 200

@campaigns_bp.route('/<int:result_id>/track/open', methods=['POST'])
def track_open(result_id):
    result = PhishingResult.query.get_or_404(result_id)
    if not result.opened:
        result.opened = True
        db.session.commit()
    return jsonify({'message': 'Tracked open'}), 200

@campaigns_bp.route('/<int:result_id>/track/click', methods=['POST'])
def track_click(result_id):
    result = PhishingResult.query.get_or_404(result_id)
    if not result.clicked_link:
        result.clicked_link = True
        result.opened = True # Clicking implies opening
        db.session.commit()
    return jsonify({'message': 'Tracked click'}), 200
