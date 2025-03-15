from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Projeto, Orcamento

main_bp = Blueprint('main', __name__)

@main_bp.route('/projetos', methods=['POST'])
@login_required
def adicionar_projeto():
    data = request.get_json()
    medidas = data.get('medidas')
    novo_projeto = Projeto(user_id=current_user.id, medidas=medidas)
    db.session.add(novo_projeto)
    db.session.commit()
    return jsonify({"message": "Projeto adicionado com sucesso"})
