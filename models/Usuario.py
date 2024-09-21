from sql_alchemy import banco
from app import bcrypt, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(banco.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = banco.Column(banco.Integer(), primary_key=True)
    nome = banco.Column(banco.String(80), nullable=False)
    email = banco.Column(banco.String(90), nullable=False, unique=True)
    senha = banco.Column(banco.String(90), nullable=False)
    experiencia = banco.Column(banco.String(1000), nullable=False)
    linkedin = banco.Column(banco.String(90))
    perfil = banco.Column(banco.String(20), nullable=False, default='usuario')

    def __init__(self, nome, email, senhaCrypt, experiencia, linkedin=''):
        self.nome = nome
        self.email = email
        self.senhaCrypt = senhaCrypt
        self.experiencia = experiencia
        self.linkedin = linkedin

    def updateUsuario(self, nome, email, experiencia, linkedin=''):
        self.nome = nome
        self.email = email
        self.experiencia = experiencia
        self.linkedin = linkedin

    @property
    def senhaCrypt(self):
        return self.senhaCrypt
    
    @senhaCrypt.setter
    def senhaCrypt(self, senha):
        self.senha = bcrypt.generate_password_hash(senha).decode('utf-8')

    def verify_password(self, senha):
        return bcrypt.check_password_hash(self.senha, senha)

    @classmethod
    def findByEmail(cls, email):
        usuario = cls.query.filter_by(email=email).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def findByEmailAndId(cls, email, id):
        usuario = cls.query.filter_by(email=email, id=id).first()
        if usuario:
            return usuario
        return None

    def save(usuario):
        banco.session.add(usuario)
        banco.session.commit()

