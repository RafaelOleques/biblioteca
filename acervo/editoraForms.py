from django import forms
from .classes.conexao_BD import ConexaoBD
from .classes.funcoes_auxiliares import *

#Formulário padrão para uma obra
class Add_EditoraForm(forms.Form):
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
        super(Add_EditoraForm, self).__init__(*args, **kwargs)
        
        if self.acao == "editar":
            print(self.id)
            usuario = "postgres"
            senha = "admin123"

            tabela = "Editora"

            atributos = []
            atributos.append(['id_editora', 'telefone', 'endereco', 'nome'])
            
            join_ = []
            join_.append('')

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            condicao = "id_editora = %s" % self.id
    
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

        print('atributo', atributo)
        print('lista', lista_checked)

        self.fields[atributo].initial = lista_checked

    def preenche_campos_select(self, BD, tabela, atributo, condicao, join_=None):
        obra_informacoes = BD.select(tabela, atributo, where=condicao, join=join_)
        obra_informacoes= obra_informacoes[0]

        self.fields[atributo].initial = obra_informacoes[atributo]