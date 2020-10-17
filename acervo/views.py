from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .forms import ObraForm
import datetime


def obra_list(request):
    usuario = "ADICIONAR SEU USUARIO"
    senha = "ADICIONAR SUA SENHA"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    titulo = "Lista de Livros"
    tabela = "Obra"

    BD = ConexaoBD("localhost", "biblioteca", usuario, senha)

    retorno["obras"] = BD.select(tabela, "*")
    retorno["titulo"] = titulo
    BD.close()

    return render(request, 'acervo/obra_list.html', retorno)

def obra_add(request):
    usuario = "ADICIONAR SEU USUARIO"
    senha = "ADICIONAR SUA SENHA"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"
    titulo = "Livros"
    acao = "Nova "+tabela
    BD = ConexaoBD("localhost", "biblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = ObraForm(request.POST)

        if form.is_valid():
            #Pega o nome dos atributos para verificar quais vão ser adicionados
            atributos = BD.atributos_nome(tabela)
            valores = []
            atributos_aux = []

            #Salva os atributos em uma variável auxiliar para que possa excluir dentro do for 
            #os que não vão ser utilizados
            atributos_aux.extend(atributos)

            #Identifica os valores dos atributos que foram recebidos
            for atributo in atributos_aux:
                if  atributo in form.cleaned_data:
                    if isinstance(form.cleaned_data[atributo], datetime.date):
                       valores.append(form.cleaned_data[atributo].strftime("%d/%m/%Y"))
                    else:
                        valores.append(form.cleaned_data[atributo])
                else:
                    atributos.remove(atributo)

            #Salva no BD os valores recebidos
            BD.insert(tabela, atributos, valores)
            BD.close()

            #Volta para a página dos livros
            return HttpResponseRedirect('/acervo/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = ObraForm()

    retorno['form'] = form
    retorno['titulo'] = titulo
    retorno['acao'] = acao

    return render(request, 'acervo/add.html', retorno)