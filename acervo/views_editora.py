from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .editoraForms import Add_EditoraForm
import datetime

titulo_pagina = "Editoras"
linkTitulo   = "editora_list"

def formata_data_BD(data):
    nova_data = data.split('/')
    return "datetime.date(%s, %s, %s)" % nova_data[0], nova_data[1], nova_data[2]

def editora_list(request):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Editora"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['nome', 'telefone', 'endereco']

    informacoes = BD.select(tabela, atributos)

    retorno["editoras"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    BD.close()

    return render(request, 'acervo/editora_list.html', retorno)

def editora_add(request):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Editora"
    acao = "Nova "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = Add_EditoraForm(request.POST)

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
            return HttpResponseRedirect('/editora/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = Add_EditoraForm()

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def editora_detail(request, editora_nome):    
    if editora_nome is None:
        return editora_list(request)

    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Editora"

    atributos = []
    atributos.append(['id_editora', 'telefone', 'endereco', 'nome'])

    condicao = "nome = '%s'" % editora_nome
    
    join_ = []
    join_.append('')
    
    tabelas = ["editoras"]

    i = 0
    for nome_tabela in tabelas:
        retorno[nome_tabela] =  BD.select(tabela, atributos[i], where=condicao, join=join_[i])
        i += 1

    BD.close()

    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/editora_informacoes.html', retorno)