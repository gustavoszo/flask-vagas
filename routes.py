from app import app, mail_settings, mail
from flask import render_template, flash, redirect, url_for, request
from forms import CadastroForm, LoginForm, validationCadastro, validationVaga, VagaForm, EditarUsuarioForm, AlterarSenhaForm
from models.Usuario import Usuario
from models.Vaga import Vaga
from models.Inscricao import Inscricao
from flask_login import login_user, logout_user, current_user, login_required
from util.Paginacao import *
from flask_mail import Message

@app.route('/')
def home():
    if request.args:
        paginacao = resultados(int(request.args['pagina']))
    else:
        paginacao = resultados(1)

    return render_template('home.html', paginacao=paginacao)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()

    if Usuario.findByEmail(form.email.data):
        flash('Endereço de e-mail já cadastrado', category='danger')
        return redirect(url_for('cadastro'))

    if form.validate_on_submit():
        usuario = Usuario(form.nome.data, form.email.data, form.senha.data, request.form.get('experiencia'), form.linkedin.data)
        Usuario.save(usuario)
        flash('Conta criada com sucesso', category='success')
        return redirect(url_for('home'))
    
    if form.errors != {}:
        # dicionario com campo de chave e descrição como valor
        for erro in form.errors:
            validationCadastro(erro)
            

    return render_template('cadastro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.findByEmail(form.email.data)
        if usuario and usuario.verify_password(form.senha.data):
            login_user(usuario)
            flash('Login realizado com sucesso', category='success')
            return redirect(url_for('home'))
        
        flash('E-mail e/ou senha inválido(s)', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin():
    if current_user.perfil != 'admin':
        return redirect(url_for('home'))
    
    vagas = Vaga.getAll()
    return render_template('admin.html', vagas=vagas)

@app.route('/createvaga', methods=['GET', 'POST'])
@login_required
def novaVaga():
    if current_user.perfil != 'admin':
        return redirect(('home'))
    
    form = VagaForm()

    if form.validate_on_submit():
        vaga = Vaga(form.nome.data, form.localidade.data, form.moeda.data, form.salario.data, form.responsabilidades.data)
        Vaga.save(vaga)
        flash(f'Vaga {vaga.nome} criada com sucesso', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for erro in form.errors:
            validationVaga(erro)
    
    return render_template('create-vaga.html', form=form)

@app.route('/editar-vaga/<id>', methods=['GET', 'POST'])
@login_required
def editarVaga(id):
    if current_user.perfil != 'admin':
        return redirect(('home'))

    vaga = Vaga.findById(id)
    form = VagaForm()

    if form.validate_on_submit():
        vaga.updateVaga(form.nome.data, form.localidade.data, form.moeda.data, form.salario.data, form.responsabilidades.data)
        Vaga.save(vaga)
        flash(f'Vaga {vaga.nome} atualizada com sucesso', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for erro in form.errors:
            validationVaga(erro)

    return render_template('create-vaga.html', vaga=vaga, form=form)

@app.route('/excluir-vaga/<id>')
@login_required
def excluirVaga(id):
    if current_user.perfil != 'admin':
        return redirect(('home'))

    vaga = Vaga.findById(id)
    if vaga:
        Vaga.delete(vaga)
        flash('Vaga removida com sucesso', category='info')
        return redirect(url_for('admin'))
    
    flash('Ocorreu um erro ao tentar excluir a vaga', category='info')

    return render_template('home.html')

@app.route('/inscricao/<id>')
@login_required
def inscricao(id):
    vaga = Vaga.findById(id)
    
    cadastro = Inscricao.findByUsuarioAndVaga(id, current_user.id)
    if cadastro:
        flash(f'Você já se inscreveu para a vaga {vaga.nome}', category='info')
        return redirect(url_for('home'))

    return render_template('inscricao.html', usuario=current_user, vaga=vaga)

@app.route('/inscricao/<id>/confirmacao')
@login_required
def inscricao_confirmada(id):
    inscricao = Inscricao(id, current_user.id)
    Inscricao.save(inscricao)
    flash('Sua inscrição foi realizada', category='info')
    return redirect(url_for('home'))

@app.route('/editar-usuario', methods=['GET', 'POST'])
@login_required
def editar_usuario():
    form = EditarUsuarioForm()

    if form.validate_on_submit():
        usuario = Usuario.findByEmail(current_user.email)
        usuario.updateUsuario(form.nome.data, form.email.data, request.form.get('experiencia'), form.linkedin.data)
        Usuario.save(usuario)
        flash('Usuario atualizado', category='info')
        return redirect(url_for('home'))
    
    if form.errors != {}:
        for erro in form.errors:
            validationCadastro(erro)

    return render_template('editar-usuario.html', form=form)

@app.route('/inscricoes-usuario')
@login_required
def inscricoes_usuario():
    if request.args:
        paginacao = vagas_usuario(int(request.args['pagina']), current_user.id)
    else:
        paginacao = vagas_usuario(1, current_user.id)

    return render_template('inscricoes-usuario.html', paginacao=paginacao)

@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    emailUsuario = request.form.get('email')
    usuario = Usuario.findByEmail(emailUsuario)

    if request.method == 'POST':
        msg = Message(
            subject = 'Recuperação de senha',
            sender = mail_settings['MAIL_USERNAME'],
            recipients = [emailUsuario],
            body = f'''
            Acesse o link para alterar a sua senha http://127.0.0.1:5000/recuperar-senha/{emailUsuario}/alterar/{usuario.id}"
            '''
        )
        mail.send(msg)
        flash('Verifique seu e-mail para alterar a senha', category='info')

    return redirect(url_for('login'))

@app.route('/recuperar-senha/<email>/alterar/<id>', methods=['GET', 'POST'])
def alterar_senha(email, id):
    form = AlterarSenhaForm()
    usuario = Usuario.findByEmailAndId(email, id)

    if request.method == 'POST':
        if form.validate_on_submit() and usuario:
            usuario.senhaCrypt = form.conf_senha.data
            Usuario.save(usuario)
            flash('Senha alterada', category='info')
            return redirect(url_for('login'))

        if form.errors != {}:
            for erro in form.errors:
                validationCadastro(erro)

    return render_template('alterar-senha.html', form=form)