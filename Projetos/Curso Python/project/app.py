from flask import Flask, request, jsonify, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marmoraria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session

db = SQLAlchemy(app)


# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email, "admin": self.admin}


class Acabamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    materiais = db.relationship('MaterialAcabamento', backref='acabamento', lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    acabamentos = db.relationship('MaterialAcabamento', backref='material', lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}


class MaterialAcabamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    acabamento_id = db.Column(db.Integer, db.ForeignKey('acabamento.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "material_id": self.material_id, "acabamento_id": self.acabamento_id, "valor": self.valor}


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    consultor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    produtos = db.relationship("ProjetoProduto", backref="projeto", lazy=True)
    acabamentos = db.relationship("ProjetoAcabamento", backref="projeto", lazy=True)
    materiais = db.relationship("ProjetoMaterial", backref="projeto", lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "consultor_id": self.consultor_id}


class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    frete = db.Column(db.Float, nullable=True)
    instalacao = db.Column(db.Float, nullable=True)
    cuba = db.Column(db.Float, nullable=True)
    desconto = db.Column(db.Float, nullable=True)
    prazo_entrega = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')

    def to_dict(self):
        return {
            "id": self.id,
            "projeto_id": self.projeto_id,
            "frete": self.frete,
            "instalacao": self.instalacao,
            "cuba": self.cuba,
            "desconto": self.desconto,
            "prazo_entrega": self.prazo_entrega,
            "status": self.status,
        }


class ProjetoProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "projeto_id": self.projeto_id, "produto_id": self.produto_id, "quantidade": self.quantidade}


class ProjetoAcabamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    acabamento_id = db.Column(db.Integer, db.ForeignKey("acabamento.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "projeto_id": self.projeto_id, "acabamento_id": self.acabamento_id}


class ProjetoMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    material_acabamento_id = db.Column(db.Integer, db.ForeignKey("material_acabamento.id"), nullable=False)
    material_acabamento = db.relationship('MaterialAcabamento', backref="projeto_materials")

    def to_dict(self):
        return {"id": self.id, "projeto_id": self.projeto_id, "material_acabamento_id": self.material_acabamento_id}


# Helper Functions
def hash_password(password):
    return generate_password_hash(password)


# Blueprints and Routes

user_bp = Blueprint("user_routes", __name__, url_prefix="/api/users")
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Autenticação necessária."}), 401
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Autenticação necessária."}), 401
        user = User.query.get(session["user_id"])
        if not user.admin:
            return jsonify({"error": "Permissão negada. Apenas administradores podem realizar esta ação."}), 403
        return f(*args, **kwargs)

    return decorated_function

@user_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    admin = data.get("admin", False)

    if not nome or not senha:
        return jsonify({"error": "Nome e senha são obrigatórios"}), 400

    # Aqui, a senha é hashada antes de ser armazenada
    hashed_senha = hash_password(senha)

    new_user = User(nome=nome, email=email, senha=hashed_senha, admin=admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário cadastrado com sucesso."}), 201

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    nome = data.get("nome")
    senha = data.get("senha")

    user = User.query.filter_by(nome=nome).first()

    if user and check_password_hash(user.senha, senha):
        session["user_id"] = user.id
        return jsonify({"message": "Login realizado com sucesso."}), 200
    else:
        return jsonify({"error": "Credenciais inválidas."}), 401

@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logout realizado com sucesso."}), 200


@user_bp.route("/list", methods=["GET"])
@login_required
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@user_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    admin = data.get("admin")

    user = User.query.get_or_404(user_id)

    if not nome or not email or not senha:
        return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400

    user.nome = nome
    user.email = email
    if senha:
        user.senha = hash_password(senha)
    user.admin = admin if admin is not None else user.admin
    db.session.commit()

    return jsonify({"message": "Usuário atualizado."})


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuário deletado com sucesso."}), 200


# Acabamentos
acabamento_bp = Blueprint("acabamento_routes", __name__, url_prefix="/api/acabamentos")


@acabamento_bp.route("/create", methods=["POST"])
def create_acabamento():
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    new_acabamento = Acabamento(nome=nome)
    db.session.add(new_acabamento)
    db.session.commit()

    return jsonify(new_acabamento.to_dict()), 201


@acabamento_bp.route("/<int:acabamento_id>", methods=["PUT"])
def update_acabamento(acabamento_id):
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    acabamento = Acabamento.query.get_or_404(acabamento_id)
    acabamento.nome = nome
    db.session.commit()

    return jsonify({"message": "Acabamento atualizado com sucesso.", "acabamento": acabamento.to_dict()}), 200


@acabamento_bp.route("/list", methods=["GET"])
def list_acabamentos():
    acabamentos = Acabamento.query.all()
    return jsonify([a.to_dict() for a in acabamentos])


# Materiais
material_bp = Blueprint("material_routes", __name__, url_prefix="/api/materiais")


@material_bp.route("/create", methods=["POST"])
def create_material():
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    new_material = Material(nome=nome)
    db.session.add(new_material)
    db.session.commit()

    return jsonify(new_material.to_dict()), 201


@material_bp.route("/<int:material_id>", methods=["PUT"])
def update_material(material_id):
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    material = Material.query.get_or_404(material_id)
    material.nome = nome
    db.session.commit()

    return jsonify({"message": "Material atualizado com sucesso.", "material": material.to_dict()}), 200


@material_bp.route("/list", methods=["GET"])
def list_materiais():
    materiais = Material.query.all()
    return jsonify([m.to_dict() for m in materiais])


# MaterialAcabamento
@material_bp.route("/<int:material_id>/acabamentos", methods=["POST"])
def create_material_acabamento(material_id):
    data = request.get_json()
    acabamento_id = data.get("acabamento_id")
    valor = data.get("valor")

    if not acabamento_id or valor is None:
        return jsonify({"error": "Acabamento ID e valor são obrigatórios"}), 400

    material_acabamento = MaterialAcabamento(material_id=material_id, acabamento_id=acabamento_id, valor=valor)
    db.session.add(material_acabamento)
    db.session.commit()

    return jsonify(material_acabamento.to_dict()), 201


@material_bp.route("/<int:material_id>/acabamentos", methods=["GET"])
def list_material_acabamentos(material_id):
    material_acabamentos = MaterialAcabamento.query.filter_by(material_id=material_id).all()
    return jsonify([ma.to_dict() for ma in material_acabamentos])


# Produtos
produto_bp = Blueprint("produto_routes", __name__, url_prefix="/api/produtos")

@produto_bp.route("/create", methods=["POST"])
def create_produto():
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    new_produto = Produto(nome=nome)
    db.session.add(new_produto)
    db.session.commit()

    return jsonify(new_produto.to_dict()), 201


@produto_bp.route("/<int:produto_id>", methods=["PUT"])
def update_produto(produto_id):
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"error": "Nome á obrigatório"}), 400

    produto = Produto.query.get_or_404(produto_id)
    produto.nome = nome
    db.session.commit()

    return jsonify({"message": "Produto atualizado com sucesso.", "produto": produto.to_dict()}), 200


@produto_bp.route("/list", methods=["GET"])
def list_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])


# Projetos
projeto_bp = Blueprint("projeto_routes", __name__, url_prefix="/api/projetos")

@projeto_bp.route("/create", methods=["POST"])
def create_projeto():
    data = request.get_json()
    nome = data.get("nome")
    consultor_id = data.get("consultor_id")

    if not nome or not consultor_id:
        return jsonify({"error": "Nome e Consultor ID são obrigatórios"}), 400

    new_projeto = Projeto(nome=nome, consultor_id=consultor_id)
    db.session.add(new_projeto)
    db.session.commit()

    return jsonify(new_projeto.to_dict()), 201


@projeto_bp.route("/list", methods=["GET"])
def list_projetos():
    projetos = Projeto.query.all()
    return jsonify([p.to_dict() for p in projetos])


@projeto_bp.route("/<int:projeto_id>/produtos", methods=["POST"])
def add_produto_to_projeto(projeto_id):
    data = request.get_json()
    produto_id = data.get("produto_id")
    quantidade = data.get("quantidade")

    if not produto_id or not quantidade:
        return jsonify({"error": "Produto ID e quantidade são obrigatórios"}), 400

    new_projeto_produto = ProjetoProduto(projeto_id=projeto_id, produto_id=produto_id, quantidade=quantidade)
    db.session.add(new_projeto_produto)
    db.session.commit()

    return jsonify(new_projeto_produto.to_dict()), 201


@projeto_bp.route("/<int:projeto_id>/acabamentos", methods=["POST"])
def add_acabamento_to_projeto(projeto_id):
    data = request.get_json()
    acabamento_id = data.get("acabamento_id")

    if not acabamento_id:
        return jsonify({"error": "Acabamento ID é obrigatório"}), 400

    new_projeto_acabamento = ProjetoAcabamento(projeto_id=projeto_id, acabamento_id=acabamento_id)
    db.session.add(new_projeto_acabamento)
    db.session.commit()

    return jsonify(new_projeto_acabamento.to_dict()), 201


@projeto_bp.route("/<int:projeto_id>/materiais", methods=["POST"])
def add_material_to_projeto(projeto_id):
    data = request.get_json()
    material_acabamento_id = data.get("material_acabamento_id")

    if not material_acabamento_id:
        return jsonify({"error": "Material Acabamento ID é obrigatório"}), 400

    new_projeto_material = ProjetoMaterial(projeto_id=projeto_id, material_acabamento_id=material_acabamento_id)
    db.session.add(new_projeto_material)
    db.session.commit()

    return jsonify(new_projeto_material.to_dict()), 201


# Orçamentos
orcamento_bp = Blueprint("orcamento_routes", __name__, url_prefix="/api/orcamentos")


@orcamento_bp.route("/create", methods=["POST"])
def create_orcamento():
    data = request.get_json()
    projeto_id = data.get("projeto_id")
    frete = data.get("frete")
    instalacao = data.get("instalacao")
    cuba = data.get("cuba")
    desconto = data.get("desconto")
    prazo_entrega = data.get("prazo_entrega")
    status = data.get("status", "Pendente")

    if not projeto_id:
        return jsonify({"error": "Projeto ID é obrigatório"}), 400

    try:
        projeto_id = int(projeto_id)
    except ValueError:
        return jsonify({"error": "Projeto ID deve ser um número inteiro"}), 400

    new_orcamento = Orcamento(projeto_id=projeto_id, frete=frete, instalacao=instalacao,
                              cuba=cuba, desconto=desconto, prazo_entrega=prazo_entrega, status=status)
    db.session.add(new_orcamento)
    db.session.commit()

    return jsonify(new_orcamento.to_dict()), 201


@orcamento_bp.route("/list", methods=["GET"])
def list_orcamentos():
    orcamentos = Orcamento.query.all()
    return jsonify([o.to_dict() for o in orcamentos])


@orcamento_bp.route("/<int:orcamento_id>", methods=["PUT"])
def update_orcamento_status(orcamento_id):
    data = request.get_json()
    status = data.get("status")

    orcamento = Orcamento.query.get_or_404(orcamento_id)

    if not status:
        return jsonify({"error": "Status é obrigatório"}), 400

    orcamento.status = status
    db.session.commit()

    return jsonify(orcamento.to_dict())


# Registering blueprints
app.register_blueprint(acabamento_bp)
app.register_blueprint(material_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(projeto_bp)
app.register_blueprint(orcamento_bp)
app.register_blueprint(user_bp)

# Running the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
