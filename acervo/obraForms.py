from django import forms
from .classes.conexao_BD import ConexaoBD

#Formulário padrão para uma obra
class Add_ObraForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    titulo = forms.CharField(label='Título', max_length=100)
    isbn = forms.CharField(label='ISBN', max_length=100)
    ano_publicacao = forms.DateField(label="Ano de publicação")
    
    autor = BD.select("Autor", ["id_autor", "nome"], nome_atributo=False)
    id_autor = forms.ChoiceField(label='Autor', widget=forms.Select, choices=autor)

    editoras = BD.select("Editora", ["id_editora", "nome"], nome_atributo=False)
    id_editora = forms.ChoiceField(label='Editora', widget=forms.Select, choices=editoras)

    generos = BD.select("Genero", ["id_genero", "nome"], nome_atributo=False)
    id_genero = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=generos,
        label="Gênero",
    )

    palavra_chave = BD.select("Palavras_chaves", ["id_palavra_chave", "nome"], nome_atributo=False)
    id_palavra_chave = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=palavra_chave,
        label="Palavras Chaves",
    )

    BD.close()