from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para um exemplar
class ExemplarForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)
    # data_nascimento = forms.DateField(label="Data de Nascimento")
    # data_falecimento = forms.DateField(label="Data de Falecimento", required=False)
    # nacionalidade = forms.CharField(label='Nacionalidade', max_length=100)
    # biografia = forms.CharField(label='Biografia', max_length=300)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(ExemplarForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            usuario = "postgres"
            senha = "admin123"

            tabela = "Exemplar"

            atributos = []
            atributos.append(['nome', 'data_nascimento', 'data_falecimento', 'nacionalidade', 'biografia'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "sequencia = %s" % self.id

            AUTOR          = 0

            self.preenche_campos_texto(BD, tabela, atributos[AUTOR], condicao, join_[AUTOR])
    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        exemplar_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        exemplar_informacoes = exemplar_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = exemplar_informacoes[atributo]