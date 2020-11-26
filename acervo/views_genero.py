from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .generoForms import GeneroForm
import datetime

titulo_pagina = "Generos"
linkTitulo   = "genero_list"

def formata_data_BD(data):
    nova_data = data.split('/')
    return "datetime.date(%s, %s, %s)" % nova_data[0], nova_data[1], nova_data[2]

def genero_list(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Genero"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['id_genero as id', 'nome']

    informacoes = BD.select(tabela, atributos)

    retorno["generos"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    BD.close()

    return render(request, 'acervo/genero_list.html', retorno)

def genero_add(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Genero"
    acao = "Novo "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = GeneroForm(request.POST, acao='adicionar', id='2')

        if form.is_valid():

            #Identifica os valores dos atributos que foram recebidos
            i = 0
            atributos_aux = []

            #Informações do Genero
            tabela = "Genero"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações do Genero para add no BD
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

            #ID do último genero adicionado
            ultimo_add = BD.ultimo_adicionado("Genero", "id_genero") + 1
            
            #Insere o novo genero no BD
            BD.insert(tabela, atributo_, valores)

            BD.close()
            

            #Volta para a página dos generos
            return HttpResponseRedirect('/genero/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = GeneroForm(acao='adicionar', id='2')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def genero_delete(request, genero_id):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    tabela = "Genero"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    retorno["titulo"] = "Not Found - Retorne ao Acervo"
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    condicao = "id_genero = %s" % genero_id
    
    BD.delete(tabela, condicao)

    return genero_list(request)

def genero_edit(request, genero_id):   
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Genero"
    acao = "Edição - "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = GeneroForm(request.POST, acao='editar', id=genero_id)

        if form.is_valid():
            tabelas = []
            tabelas_n = []
            atributos = []

            #Pega o nome dos atributos para verificar quais vão ser adicionados
            for tabela in tabelas:
                atributos.append(BD.atributos_nome(tabela))

            atualizacoes = []
            

            #Salva os atributos em uma variável auxiliar para que possa excluir dentro do for 
            #os que não vão ser utilizados

            #Identifica os valores dos atributos que foram recebidos
            i = 0
            atributos_aux = []
            
            #Dicionário para saber qual tabela está ligando a primeira com Genero
            tabela_relacoes = {
            }

            #Dicionário para saber qual é o id de cada tabela
            id_genero = "id_genero"

            #Informações da Genero
            tabela = "Genero"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            atualizacoes = []

            #Pega as informações da Genero para add no BD
            for atributo in atributos_aux:
                if atributo in form.cleaned_data:
                    if isinstance(form.cleaned_data[atributo], datetime.date):
                        formata_update = "{0} = '{1}'".format(atributo, form.cleaned_data[atributo].strftime("%d/%m/%Y"))
                        atualizacoes.append(formata_update)
                    elif "id_" in atributo:
                        formata_update = "{0} = {1}".format(atributo, form.cleaned_data[atributo])
                        atualizacoes.append(formata_update)
                    else:
                        if type(form.cleaned_data[atributo]) is list:
                            for lista in form.cleaned_data[atributo]:
                                formata_update = "{0} = '{1}'".format(atributo, lista)
                                atualizacoes.append(formata_update)
                        else:
                            formata_update = "{0} = '{1}'".format(atributo, form.cleaned_data[atributo])
                            atualizacoes.append(formata_update)
                else:
                    atributo_.remove(atributo)

            atualizacoes = ', '.join(atualizacoes)
            condicao = "{0} = {1}".format(id_genero, genero_id)

            #Atualiza a genero
            BD.update(tabela, atualizacoes, condicao)


            atributos_aux = []
            atualizacoes = []

            #Pega os valores e atributos dos demais que fazem relação com genero
            for tabela in tabelas:
                atributos_aux.extend(atributos[i])
                for atributo in atributos[i]:
                    if atributo in form.cleaned_data:
                        if type(form.cleaned_data[atributo]) is list:
                            for lista in form.cleaned_data[atributo]:
                                atualizacoes.append(lista)
                        else:
                            atualizacoes.append(form.cleaned_data[atributo])
                    else:
                        atributos_aux.remove(atributo)
                
                #Deleta as relações que já haviam
                i += 1
                for valor in atualizacoes:
                    tabela_atualiza = tabela_relacoes[tabela]

                    condicao = "{0} = {1}".format(id_genero, genero_id)
                    BD.delete(tabela_atualiza, condicao)

                #Adiciona as novas relações
                for valor in atualizacoes:
                    tabela_atualiza = tabela_relacoes[tabela]

                    atributos_add = [id_genero, atributos_aux[0]]
                    valores_add = [genero_id, valor]
                    BD.insert(tabela_atualiza, atributos_add, valores_add)
                    

                atributos_aux = []
                atualizacoes = []
                
            
            BD.close()
            

            #Volta para a página dos generos
            return HttpResponseRedirect('/genero/{0}'.format(genero_id))

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = GeneroForm(acao='editar', id=genero_id)

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def genero_detail(request, genero_id):   
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')
         
    if genero_id is None:
        return genero_list(request)

    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Genero"

    atributos = []
    atributos.append(['id_genero as id', 'nome'])
    atributos.append(['id_obra as id','Obra.titulo as titulo'])

    condicao = "id_genero = %s" % genero_id
    
    join_ = []
    join_.append('')
    join_.append("JOIN Classificacao USING(id_genero) " + "JOIN Obra USING(id_obra)")
    
    tabelas = ["generos", "obras"]    

    i = 0
    for nome_tabela in tabelas:
        retorno[nome_tabela] =  BD.select(tabela, atributos[i], where=condicao, join=join_[i])
        i += 1

    BD.close()

    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/genero_informacoes.html', retorno)