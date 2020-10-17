from django import forms
from .classes.conexao_BD import ConexaoBD

#Formulário padrão para uma obra
class ObraForm(forms.Form):
    usuario = "ADICIONAR SEU USUARIO"
    senha = "ADICIONAR SUA SENHA"

    titulo = forms.CharField(label='Título', max_length=100)
    isbn = forms.CharField(label='ISBN', max_length=100)
    
    BD = ConexaoBD("localhost", "biblioteca", usuario, senha)
    Options = BD.select("Editora", ["id_editora", "nome"], nome_atributo=False)
    BD.close()
    
    id_editora = forms.ChoiceField(label='Editora', widget=forms.Select, choices=Options)
    ano_publicacao = forms.DateField()
