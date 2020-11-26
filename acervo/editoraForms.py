from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para uma editora
class EditoraForm(forms.Form):
    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    nome = forms.CharField(label='Nome', max_length=100)
    telefone = forms.CharField(label='Telefone', max_length=100)
    endereco = forms.CharField(label='Endereço', max_length=100)

    BD.close()

    def __init__(self, *args, **kwargs):
        self.acao = kwargs.pop('acao', None)
        self.id = kwargs.pop('id', None)
        super(EditoraForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            usuario = "postgres"
            senha = "admin123"

            tabela = "Editora"

            atributos = []
            atributos.append(['telefone', 'endereco', 'nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_editora = %s" % self.id

            EDITORA          = 0

            self.preenche_campos_texto(BD, tabela, atributos[EDITORA], condicao, join_[EDITORA])

    
    def preenche_campos_texto(self, BD, tabela, atributos, condicao, join_=None):
        editora_informacoes = BD.select(tabela, atributos, where=condicao, join=join_)
        editora_informacoes = editora_informacoes[0]

        atributos = valida_lista(atributos)

        for atributo in atributos:
            self.fields[atributo].widget.attrs['value'] = editora_informacoes[atributo]