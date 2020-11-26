from django import forms
from .classes.conexao_BD import ConexaoBD

class UsuarioLoginForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    usuarios = BD.select("Usuario", ["codigo", "email"], nome_atributo=False)
    print(usuarios)
    id_usuario = forms.ChoiceField(label='Usuario', widget=forms.Select, choices=usuarios)

    def __init__(self, *args, **kwargs):
        super(UsuarioLoginForm, self).__init__(*args, **kwargs)


#Formulário padrão para adicionar/editar um usuário
class UsuarioForm(forms.Form):
    
    nome  = forms.CharField(label='Nome', max_length=60)
    email  = forms.CharField(label='Email', max_length=60)
    senha  = forms.CharField(label='Senha', max_length=60, widget=forms.PasswordInput)
    endereco  = forms.CharField(label='Endereco', max_length=100)
    telefone  = forms.CharField(label='Telefone', max_length=12)

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(UsuarioForm, self).__init__(*args, **kwargs)