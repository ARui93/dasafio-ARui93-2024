from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from auth_routes import auth_bp
from main_routes import main_bp
from admin_routes import admin_bp

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testproject'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Orcamento.db'
    
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
