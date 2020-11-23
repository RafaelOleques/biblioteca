from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para um autor
class Add_AutorForm(forms.Form):
    usuario = "postgres"
    senha = "admin13"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)
    data_nascimento = forms.DateField(label="Data de Nascimento")
    data_falecimento = forms.DateField(label="Data de Falecimento")
    nacionalidade = forms.CharField(label='Nacionalidade', max_length=100)
    biografia = forms.CharField(label='Biografia', max_length=300)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(Add_AutorForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            print(self.id)
            usuario = "postgres"
            senha = "admin13"

            tabela = "Autor"

            atributos = []
            atributos.append(['id_autor', 'nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_autor = %s" % self.id
    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        autor_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        autor_informacoes = autor_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = autor_informacoes[atributo]
    
    def preenche_campos_checkbox(self, BD, tabela, atributo, condicao, join_=None):
        autor_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)

        lista_checked = []

        for informacoes in autor_informacoes:
            lista_checked.append(informacoes[atributo])

        print('atributo', atributo)
        print('lista', lista_checked)

        self.fields[atributo].initial = lista_checked

    def preenche_campos_select(self, BD, tabela, atributo, condicao, join_=None):
        autor_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)
        autor_informacoes= autor_informacoes[0]

        self.fields[atributo].initial = autor_informacoes[atributo]