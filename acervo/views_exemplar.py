from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .exemplarForms import ExemplarForm
import datetime

titulo_pagina = "Livros do Acervo"
linkTitulo   = "obra_list"


def exemplar_add(request, obra_id):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Exemplar"
    acao = "Adição - "+ tabela

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['sequencia as id', 'edicao']

    informacoes = BD.select(tabela, atributos)

    retorno["exemplares"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    BD.close()

    return render(request, 'acervo/exemplar_list.html', retorno)

def exemplar_add(request):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Exemplar"
    acao = "Novo "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = ExemplarForm(request.POST, acao='adicionar', id='2')

        if form.is_valid():
            tabelas = ["Obra", "Sub_Biblioteca"]
            atributos = []

            #Pega o nome dos atributos para verificar quais vão ser adicionados
            for tabela in tabelas:
                atributos.append(BD.atributos_nome(tabela))

            valores = []
            

            #Salva os atributos em uma variável auxiliar para que possa excluir dentro do for 
            #os que não vão ser utilizados

            #Identifica os valores dos atributos que foram recebidos
            i = 0
            atributos_aux = []

            #Informações do Exemplar
            tabela = "Exemplar"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações do Exemplar para add no BD
            for atributo in atributos_aux:
                if atributo in form.cleaned_data:
                    if "id_" in atributo:
                        valores.append(form.cleaned_data[atributo])
                    else:
                        if type(form.cleaned_data[atributo]) is list:
                            for lista in form.cleaned_data[atributo]:
                                valores.append(lista)
                        else:
                            valores.append(form.cleaned_data[atributo])
                else:
                    atributo_.remove(atributo)

            #atributo_.append("id_obra")
            #valores.append(obra_id)
            
            #Insere o novo obra no BD
            #ID do último exemplar adicionado
            ultimo_add = BD.ultimo_adicionado("Exemplar", "sequencia") + 1
            
            #Insere o novo exemplar no BD
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            BD.close()
            

            #Volta para a página dos livros
            return HttpResponseRedirect('/acervo/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = ExemplarForm(acao='adicionar', id='2')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = tabela.lower() + "_add"

    return render(request, 'acervo/add.html', retorno)
