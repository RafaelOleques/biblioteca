from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *


#Formulário padrão para uma obra
class ExemplarForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #numérico
    edicao = forms.CharField(label='Título', max_length=100)
    
    subBiblitecas = BD.select("Sub_Biblioteca", ["id_subBiblioteca", "nome"], nome_atributo=False)
    id_subBiblioteca = forms.ChoiceField(label='Sub-Biblioteca', widget=forms.Select, choices=subBiblitecas)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(ExemplarForm, self).__init__(*args, **kwargs)
        '''
        if self.acao == "editar":
            usuario = "postgres"
            senha = "admin123"

            tabela = "Obra"

            atributos = []
            atributos.append(['isbn', 'titulo', 'ano_publicacao'])
            atributos.append('id_autor')
            atributos.append('id_genero')
            atributos.append('id_palavra_chave')
            atributos.append('id_editora')
            
            join_ = []
            join_.append('')
            join_.append("JOIN Autoria USING(id_obra) " + "JOIN Autor USING(id_autor)")
            join_.append("JOIN Classificacao USING(id_obra) " + "JOIN Genero USING (id_genero)")
            join_.append("JOIN Assunto USING(id_obra)" + "JOIN Palavras_Chaves USING (id_palavra_chave)")
            join_.append("JOIN Editora USING (id_editora)")

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_obra = %s" % self.id 

            OBRA          = 0
            AUTOR         = 1
            GENERO        = 2
            PALAVRA_CHAVE = 3
            EDITORA       = 4

            self.preenche_campos_texto(BD, tabela, atributos[OBRA], condicao, join_[OBRA])
            self.preenche_campos_select(BD, tabela, atributos[AUTOR], condicao, join_[AUTOR])
            self.preenche_campos_checkbox(BD, tabela, atributos[GENERO], condicao, join_[GENERO])
            self.preenche_campos_checkbox(BD, tabela, atributos[PALAVRA_CHAVE], condicao, join_[PALAVRA_CHAVE])
            self.preenche_campos_select(BD, tabela, atributos[EDITORA], condicao, join_[EDITORA])

        '''
    '''
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        obra_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        obra_informacoes = obra_informacoes[0]

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