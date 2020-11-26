from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para um genero
class GeneroForm(forms.Form):
    usuario = "postgres"
    senha = "#Fantasma10"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(GeneroForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            usuario = "postgres"
            senha = "#Fantasma10"

            tabela = "Genero"

            atributos = []
            atributos.append(['nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_genero = %s" % self.id

            GENERO          = 0

            self.preenche_campos_texto(BD, tabela, atributos[GENERO], condicao, join_[GENERO])
    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        genero_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        genero_informacoes = genero_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = genero_informacoes[atributo]