from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para uma palavraChave
class SubBibliotecaForm(forms.Form):
    usuario = "postgres"
    senha = "#Fantasma10"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(SubBibliotecaForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            usuario = "postgres"
            senha = "#Fantasma10"

            tabela = "Sub_Biblioteca"

            atributos = []
            atributos.append(['nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_subBiblioteca = %s" % self.id

            SUBBIBLIOTECA          = 0

            self.preenche_campos_texto(BD, tabela, atributos[SUBBIBLIOTECA], condicao, join_[SUBBIBLIOTECA])
    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        subBiblioteca_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        subBiblioteca_informacoes = subBiblioteca_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = subBiblioteca_informacoes[atributo]