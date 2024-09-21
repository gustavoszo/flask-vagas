from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired
import email_validator

class CadastroForm(FlaskForm):

    nome = StringField(label='Nome: ', validators=[Length(4), DataRequired()])
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    senha = PasswordField(label='Senha: ', validators=[Length(5), DataRequired()])
    conf_senha = PasswordField(label='Confirmar senha: ', validators=[EqualTo('senha'), DataRequired()])
    experiencia = StringField(label='Experiência: ', validators=[DataRequired()])
    linkedin = StringField(label='Linkedin: ', validators=[Length(20)])
    submit = SubmitField(label='Confirmar')

class LoginForm(FlaskForm):

    email = StringField(label='Email: ', validators=[DataRequired()])
    senha = PasswordField(label='Senha: ', validators=[DataRequired()])
    submit = SubmitField(label='Entrar')

class VagaForm(FlaskForm):

    nome = StringField(label='Nome: ', validators=[Length(4), DataRequired()])
    localidade = StringField(label='Localidade: ', validators=[Length(6), DataRequired()])
    moeda = StringField(label='Moeda: ', validators=[Length(1), DataRequired()])
    salario = FloatField(label='Salário: ', validators=[DataRequired()])
    responsabilidades = StringField(label='Responsabilidades: ', validators=[Length(10), DataRequired()])
    submit = SubmitField(label='Confirmar')


class EditarUsuarioForm(FlaskForm):

    nome = StringField(label='Nome: ', validators=[Length(4), DataRequired()])
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    experiencia = StringField(label='Experiência: ', validators=[DataRequired()])
    linkedin = StringField(label='Linkedin: ', validators=[Length(20)])
    submit = SubmitField(label='Confirmar')

class AlterarSenhaForm(FlaskForm):

    senha = PasswordField(label='Nome: ', validators=[Length(5), DataRequired()])
    conf_senha = PasswordField(label='Email: ', validators=[EqualTo('senha')])
    submit = SubmitField(label='Confirmar')

def validationCadastro(campo):
    if campo == 'email':
        flash('Endereço de e-mail inválido', category='danger')
    elif campo == 'conf_senha':
        flash('Senha e confirmação de senhas diferentes', category='danger')

def validationVaga(campo):
    if campo == 'salario':
        flash('Informe um salário válido', category='danger')