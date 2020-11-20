from django import forms
from .classes.conexao_BD import ConexaoBD

#Formulário padrão para uma obra
class Add_EditoraForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)
    telefone = forms.CharField(label='Telefone', max_length=100)
    endereco = forms.CharField(label='Endereço', max_length=100)

    BD.close()