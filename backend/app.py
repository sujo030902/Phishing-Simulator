import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db, migrate

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///phishing.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from routes.templates import templates_bp
    app.register_blueprint(templates_bp, url_prefix='/api/templates')

    from routes.campaigns import campaigns_bp
    app.register_blueprint(campaigns_bp, url_prefix='/api/campaigns')

    from routes.targets import targets_bp
    app.register_blueprint(targets_bp, url_prefix='/api/targets')


    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'phishing-simulator-backend'}

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
