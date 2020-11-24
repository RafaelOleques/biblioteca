from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para uma palavraChave
class PalavraChaveForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(PalavraChaveForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            print(self.id)
            usuario = "postgres"
            senha = "admin123"

            tabela = "Palavras_Chaves"

            atributos = []
            atributos.append(['nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_palavra_chave = %s" % self.id

            PALAVRACHAVE          = 0

            self.preenche_campos_texto(BD, tabela, atributos[PALAVRACHAVE], condicao, join_[PALAVRACHAVE])
    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        palavraChave_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        palavraChave_informacoes = palavraChave_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = palavraChave_informacoes[atributo]