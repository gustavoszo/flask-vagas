from sql_alchemy import banco

class Vaga(banco.Model):
    __tablename__= 'vagas'

    id = banco.Column(banco.Integer(), primary_key=True)
    nome = banco.Column(banco.String(80), nullable = False)
    localidade = banco.Column(banco.String(45), nullable=False)
    moeda = banco.Column(banco.String(5), nullable=False)
    salario = banco.Column(banco.Float(precision=2), nullable=False)
    responsabilidades = banco.Column(banco.String(1000), nullable=False)

    def __init__(self, nome, localidade, moeda, salario, responsabilidades):
        self.nome = nome
        self.localidade = localidade
        self.moeda = moeda
        self.salario = salario
        self.responsabilidades = responsabilidades

    def updateVaga(self, nome, localidade, moeda, salario, responsabilidades):
        self.nome = nome
        self.localidade = localidade
        self.moeda = moeda
        self.salario = salario
        self.responsabilidades = responsabilidades

    @classmethod
    def getAll(cls):
        return cls.query.all()
    
    @classmethod
    def findById(cls,id):
        vaga = cls.query.filter_by(id=id).first()
        if vaga:
            return vaga
        return None
    
    def save(vaga):
        banco.session.add(vaga)
        banco.session.commit()
    
    def delete(vaga):
        banco.session.delete(vaga)
        banco.session.commit()