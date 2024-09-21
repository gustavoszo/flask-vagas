import sys
sys.path.append('C:\\Users\\Raquel\\Documents\\VSCode\\Web Flask Vagas')

from app import app
from sql_alchemy import banco

from models.Usuario import Usuario
from models.Vaga import Vaga
from models.Inscricao import Inscricao

app.app_context().push()


