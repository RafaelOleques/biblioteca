from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para um exemplar
class ExemplarForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #numérico
    edicao = forms.CharField(label='Edição', max_length=100)
    
    subBiblitecas = BD.select("Sub_Biblioteca", ["id_subBiblioteca", "nome"], nome_atributo=False)
    id_subbiblioteca = forms.ChoiceField(label='Sub-Biblioteca', widget=forms.Select, choices=subBiblitecas)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(ExemplarForm, self).__init__(*args, **kwargs)
        '''
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
            self.fields[atributo].widget.attrs['value'] = obra_informacoes[atributo]
    
    def preenche_campos_checkbox(self, BD, tabela, atributo, condicao, join_=None):
        obra_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)

        lista_checked = []

        for informacoes in obra_informacoes:
            lista_checked.append(informacoes[atributo])

        self.fields[atributo].initial = lista_checked

    def preenche_campos_select(self, BD, tabela, atributo, condicao, join_=None):
        obra_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)
        obra_informacoes= obra_informacoes[0]

        self.fields[atributo].initial = obra_informacoes[atributo]

    '''
