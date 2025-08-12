import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///church_orders.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import routes after app initialization
from routes import *

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Create admin user if not exists
    from models import Admin
    from werkzeug.security import generate_password_hash
    
    admin = Admin.query.filter_by(email='arielle.tigre@hotmail.com').first()
    if not admin:
        admin = Admin(
            email='arielle.tigre@hotmail.com',
            name='Arielle Tigre',
            password_hash=generate_password_hash('Ar@983522274')
        )
        db.session.add(admin)
        db.session.commit()
        logging.info("Admin user created successfully")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
