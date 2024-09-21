from sql_alchemy import banco

class Inscricao(banco.Model):
    __tablename__= 'inscricoes'

    id = banco.Column(banco.Integer(), primary_key=True)
    id_vaga = banco.Column(banco.Integer(), banco.ForeignKey('vagas.id'))
    id_usuario = banco.Column(banco.Integer(), banco.ForeignKey('usuarios.id'))

    def __init__(self, id_vaga, id_usuario):
        self.id_vaga = id_vaga
        self.id_usuario = id_usuario

    @classmethod
    def findByUsuarioAndVaga(cls, id_vaga, id_usuario):
        inscricao = cls.query.filter_by(id_vaga=id_vaga, id_usuario=id_usuario).first()
        if inscricao:
            return True
        return None

    def save(vaga):
        banco.session.add(vaga)
        banco.session.commit()