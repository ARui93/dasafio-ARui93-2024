from flask import Blueprint, request, jsonify
from models import User, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create-admin', methods=['POST'])
def create_admin():
    data = request.json
    email = data.get('email')
    nome = data.get('nome')
    senha = data.get('senha')
    tipo = 'ADM'  # Define o tipo de usuário como 'ADM'

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Usuário já existe"}), 400
    
    new_user = User(
        nome=nome, 
        email=email, 
        senha=senha, 
        tipo=tipo
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário administrador criado com sucesso"}), 201
