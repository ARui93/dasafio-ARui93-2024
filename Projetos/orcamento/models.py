from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    senha = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # ADM ou Consultor

    def __repr__(self):
        return f"<User {self.nome} ({self.tipo})>"

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    produtos = db.relationship('ProjetoProduto', back_populates='projeto')
    materiais = db.relationship('ProjetoMaterial', back_populates='projeto')
    acabamentos = db.relationship('ProjetoAcabamento', back_populates='projeto')
    medidas = db.Column(db.JSON, nullable=False)  # Lista de medidas para cada produto
    orcamento = db.relationship('Orcamento', uselist=False, backref='projeto')

    def calcular_valor_total(self):
        total = 0
        for projeto_produto in self.produtos:
            produto = projeto_produto.produto
            comprimento = projeto_produto.comprimento
            largura = projeto_produto.largura
            area = comprimento * largura
            for projeto_material in self.materiais:
                material = projeto_material.material
                for projeto_acabamento in self.acabamentos:
                    acabamento = projeto_acabamento.acabamento
                    custo = area * material.get_valor(acabamento.tipo)
                    total += custo
        return total

    def __repr__(self):
        return f"<Projeto ID: {self.id}, User: {self.user_id}>"

class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    frete = db.Column(db.Float, nullable=True)
    instalacao = db.Column(db.Float, nullable=True)
    cuba = db.Column(db.Float, nullable=True)
    desconto = db.Column(db.Float, nullable=True)
    prazoEntrega = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pendente')  # Aprovado ou Reprovado

    def gerar_pdf(self):
        # Lógica para gerar o PDF do orçamento
        pass

    def __repr__(self):
        return f"<Orcamento ID: {self.id}, Projeto: {self.projeto_id}>"

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    detalhes = db.Column(db.Text, nullable=True)
    projetos = db.relationship('ProjetoProduto', back_populates='produto')

    def __repr__(self):
        return f"<Produto {self.nome}>"

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    acabamentos = db.relationship('Acabamento', back_populates='material')

    def __repr__(self):
        return f"<Material {self.nome}>"

class Acabamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(80), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    material = db.relationship('Material', back_populates='acabamentos')

    def __repr__(self):
        return f"<Acabamento {self.tipo}>"

class ProjetoProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    comprimento = db.Column(db.Float, nullable=False)
    largura = db.Column(db.Float, nullable=False)
    projeto = db.relationship('Projeto', back_populates='produtos')
    produto = db.relationship('Produto', back_populates='projetos')

class ProjetoMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    projeto = db.relationship('Projeto', back_populates='materiais')
    material = db.relationship('Material', back_populates='projetos')

class ProjetoAcabamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    acabamento_id = db.Column(db.Integer, db.ForeignKey('acabamento.id'), nullable=False)
    projeto = db.relationship('Projeto', back_populates='acabamentos')
    acabamento = db.relationship('Acabamento', back_populates='projetos')
