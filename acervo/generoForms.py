from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para um genero
class Add_GeneroForm(forms.Form):
    usuario = "postgres"
    senha = "admin13"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(Add_GeneroForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            print(self.id)
            usuario = "postgres"
            senha = "admin13"

            tabela = "Genero"

            atributos = []
            atributos.append(['id_genero', 'nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_genero = %s" % self.id
    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        genero_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        genero_informacoes = genero_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = genero_informacoes[atributo]
    
    def preenche_campos_checkbox(self, BD, tabela, atributo, condicao, join_=None):
        genero_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)

        lista_checked = []

        for informacoes in genero_informacoes:
            lista_checked.append(informacoes[atributo])

        print('atributo', atributo)
        print('lista', lista_checked)

        self.fields[atributo].initial = lista_checked

    def preenche_campos_select(self, BD, tabela, atributo, condicao, join_=None):
        genero_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)
        genero_informacoes= genero_informacoes[0]

        self.fields[atributo].initial = genero_informacoes[atributo]