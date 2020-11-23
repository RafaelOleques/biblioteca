from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .palavraChaveForms import Add_PalavraChaveForm
import datetime

titulo_pagina = "Palavras Chaves"
linkTitulo   = "palavraChave_list"

def formata_data_BD(data):
    nova_data = data.split('/')
    return "datetime.date(%s, %s, %s)" % nova_data[0], nova_data[1], nova_data[2]

def palavraChave_list(request):
    usuario = "postgres"
    senha = "admin13"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Palavras_Chaves"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['id_palavra_chave as id', 'nome']

    informacoes = BD.select(tabela, atributos)

    retorno["palavrasChaves"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    BD.close()

    return render(request, 'acervo/palavraChave_list.html', retorno)

def palavraChave_add(request):
    usuario = "postgres"
    senha = "admin13"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Palavras_Chaves"
    acao = "Novas "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = Add_PalavraChaveForm(request.POST, acao='adicionar', id='2')

        if form.is_valid():
            tabelas = ["Palavras_Chaves"]
            tabelas_n = []
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
            
            #Dicionário para saber qual tabela está ligando a primeira com PalavraChave
            tabela_id = {
                }

            #Informações da PalavraChave
            tabela = "Palavras_Chaves"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações da PalavraChave para add no BD
            for atributo in atributos_aux:
                if atributo in form.cleaned_data:
                    if isinstance(form.cleaned_data[atributo], datetime.date):
                        valores.append(form.cleaned_data[atributo].strftime("%d/%m/%Y"))
                    elif "id_" in atributo:
                        valores.append(form.cleaned_data[atributo])
                    else:
                        if type(form.cleaned_data[atributo]) is list:
                            for lista in form.cleaned_data[atributo]:
                                valores.append(lista)
                        else:
                            valores.append(form.cleaned_data[atributo])
                else:
                    atributo_.remove(atributo)

            #ID da última palavraChave adicionada
            ultimo_add = BD.ultimo_adicionado("PalavraChave", "id_palavra_chave") + 1
            
            #Insere a nova palavraChave no BD
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            BD.close()
            

            #Volta para a página das palavrasChaves
            return HttpResponseRedirect('/palavraChave/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = Add_PalavraChaveForm(acao='adicionar', id='2')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def palavraChave_delete(request, palavraChave_id):
    usuario = "postgres"
    senha = "admin13"

    tabela = "Palavras_Chaves"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    retorno["titulo"] = "Not Found - Retorne ao Acervo"
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    condicao = "id_palavra_chave = %s" % palavraChave_id
    
    BD.delete(tabela, condicao)

    return palavraChave_list(request)

def palavraChave_edit(request, palavraChave_id):    
    usuario = "postgres"
    senha = "admin13"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Palavras_Chaves"
    acao = "Novas "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = Add_PalavraChaveForm(request.POST, acao='editar', id=palavraChave_id)

        if form.is_valid():
            tabelas = ["Palavras_Chaves"]
            tabelas_n = []
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
            
            #Dicionário para saber qual tabela está ligando a primeira com PalavraChave
            tabela_id = {
                }

            #Informações da PalavraChave
            tabela = "Palavras_Chaves"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações da PalavraChave para add no BD
            for atributo in atributos_aux:
                if atributo in form.cleaned_data:
                    if isinstance(form.cleaned_data[atributo], datetime.date):
                        valores.append(form.cleaned_data[atributo].strftime("%d/%m/%Y"))
                    elif "id_" in atributo:
                        valores.append(form.cleaned_data[atributo])
                    else:
                        if type(form.cleaned_data[atributo]) is list:
                            for lista in form.cleaned_data[atributo]:
                                valores.append(lista)
                        else:
                            valores.append(form.cleaned_data[atributo])
                else:
                    atributo_.remove(atributo)

            #ID da última palavraChave adicionada
            #ultimo_add = BD.ultimo_adicionado("PalavraChave", "id_palavra_chave") + 1
            
            #Insere o novo palavraChave no BD
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            #Pega os valores e atributos dos demais que fazem relação com palavraChave
            for tabela in tabelas:
                atributos_aux.extend(atributos[i])
                for atributo in atributos[i]:
                    if atributo in form.cleaned_data:
                        if isinstance(form.cleaned_data[atributo], datetime.date):
                            valores.append(form.cleaned_data[atributo].strftime("%d/%m/%Y"))
                        else:
                            if type(form.cleaned_data[atributo]) is list:
                                for lista in form.cleaned_data[atributo]:
                                    valores.append(lista)
                            else:
                                valores.append(form.cleaned_data[atributo])
                    else:
                        atributos_aux.remove(atributo)
                
                #Adiciona no BD as relações
                i += 1
                for valor in valores:
                    tabela_add = tabela_id[tabela]
                    atributos_add = ["id_palavra_chave", atributos_aux[0]]
                    valores_add = [ultimo_add,valor]

                    #BD.insert(tabela_add, atributos_add, valores_add)

                atributos_aux = []
                valores = []

            BD.close()
            

            #Volta para a página das palavrasChaves
            return HttpResponseRedirect('/palavraChave/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = Add_PalavraChaveForm(acao='editar', id=palavraChave_id)

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def palavraChave_detail(request, palavraChave_id):    
    if palavraChave_id is None:
        return palavraChave_list(request)

    usuario = "postgres"
    senha = "admin13"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Palavras_Chaves"

    atributos = []
    atributos.append(['id_palavra_chave as id', 'nome'])

    condicao = "id_palavra_chave = %s" % palavraChave_id
    
    join_ = []
    join_.append('')

    tabelas = ["Palavras_Chaves"]

    i = 0
    for nome_tabela in tabelas:
        retorno[nome_tabela] =  BD.select(tabela, atributos[i], where=condicao, join=join_[i])
        i += 1

    BD.close()

    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/palavraChave_informacoes.html', retorno)