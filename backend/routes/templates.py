from flask import Blueprint, request, jsonify
from services.gemini_service import gemini_service
from models import EmailTemplate
from extensions import db
import json

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/generate', methods=['POST'])
def generate_template_api():
    data = request.get_json()
    template_type = data.get('type')
    sender_name = data.get('sender_name')
    context = data.get('context', '')
    
    if not template_type:
        return jsonify({'error': 'Template type is required'}), 400
        
    generated_content = gemini_service.generate_template(template_type, sender_name, context)
    
    if generated_content:
        return jsonify(generated_content)
    else:
        return jsonify({'error': 'Failed to generate template'}), 500

@templates_bp.route('/', methods=['GET'])
def get_templates():
    templates = EmailTemplate.query.all()
    result = []
    for t in templates:
        result.append({
            'id': t.id,
            'name': t.name,
            'subject': t.subject,
            'body_content': t.body_content,
            'is_ai_generated': t.is_ai_generated
        })
    return jsonify(result)

@templates_bp.route('/', methods=['POST'])
def save_template():
    data = request.get_json()
    
    new_template = EmailTemplate(
        name=data.get('name', 'Untitled Template'),
        subject=data.get('subject'),
        body_content=data.get('body_content') or data.get('body'), # Handle both keys
        is_ai_generated=data.get('is_ai_generated', False),
        created_by=data.get('user_id') # Optional for now
    )

    db.session.add(new_template)
    db.session.commit()
    
    return jsonify({'message': 'Template saved', 'id': new_template.id}), 201

@templates_bp.route('/<int:id>', methods=['PUT'])
def update_template(id):
    template = EmailTemplate.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        template.name = data['name']
    
    db.session.commit()
    return jsonify({'message': 'Template updated'}), 200

    db.session.delete(template)
    db.session.commit()
    return jsonify({'message': 'Template deleted'}), 200

@templates_bp.route('/analyze', methods=['POST'])
def analyze_email():
    data = request.get_json()
    subject = data.get('subject')
    body = data.get('body')
    
    if not subject or not body:
        return jsonify({'error': 'Subject and Body required'}), 400
        
    analysis = gemini_service.analyze_template(subject, body)
    return jsonify({'analysis': analysis})
