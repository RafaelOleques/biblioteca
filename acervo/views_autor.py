from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .autorForms import AutorForm
import datetime

titulo_pagina = "Autores"
linkTitulo   = "autor_list"

def formata_data_BD(data):
    nova_data = data.split('/')
    return "datetime.date(%s, %s, %s)" % nova_data[0], nova_data[1], nova_data[2]

def autor_list(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Autor"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['id_autor as id', 'nome', 'data_nascimento', 'data_falecimento', 'nacionalidade', 'biografia']

    informacoes = BD.select(tabela, atributos)

    retorno["autores"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    BD.close()

    return render(request, 'acervo/autor_list.html', retorno)

def autor_add(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Autor"
    acao = "Novo "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = AutorForm(request.POST, acao='adicionar', id='2')

        if form.is_valid():
            tabelas = []
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
            
            #Dicionário para saber qual tabela está ligando a primeira com Autor
            tabela_id = {
                }

            #Informações do Autor
            tabela = "Autor"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações do Autor para add no BD
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

            #ID do último autor adicionado
            ultimo_add = BD.ultimo_adicionado("Autor", "id_autor") + 1
            
            #Insere o novo autor no BD
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            #Pega os valores e atributos dos demais que fazem relação com autor
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
                    atributos_add = ["id_autor", atributos_aux[0]]
                    valores_add = [ultimo_add,valor]

                    BD.insert(tabela_add, atributos_add, valores_add)

                atributos_aux = []
                valores = []

            BD.close()
            

            #Volta para a página dos autores
            return HttpResponseRedirect('/autor/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = AutorForm(acao='adicionar', id='2')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def autor_delete(request, autor_id):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    tabela = "Autor"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    retorno["titulo"] = "Not Found - Retorne ao Acervo"
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    condicao = "id_autor = %s" % autor_id
    
    BD.delete(tabela, condicao)

    return autor_list(request)

def autor_edit(request, autor_id):    
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Autor"
    acao = "Edição - "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = AutorForm(request.POST, acao='editar', id=autor_id)

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
            
            #Dicionário para saber qual tabela está ligando a primeira com Autor
            tabela_relacoes = {
            }

            #Dicionário para saber qual é o id de cada tabela
            id_autor = "id_autor"

            #Informações da Autor
            tabela = "Autor"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            atualizacoes = []

            #Pega as informações da Autor para add no BD
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
            condicao = "{0} = {1}".format(id_autor, autor_id)

            #Atualiza a autor
            BD.update(tabela, atualizacoes, condicao)


            atributos_aux = []
            atualizacoes = []

            #Pega os valores e atributos dos demais que fazem relação com autor
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

                    condicao = "{0} = {1}".format(id_autor, autor_id)
                    BD.delete(tabela_atualiza, condicao)

                #Adiciona as novas relações
                for valor in atualizacoes:
                    tabela_atualiza = tabela_relacoes[tabela]

                    atributos_add = [id_autor, atributos_aux[0]]
                    valores_add = [autor_id, valor]
                    BD.insert(tabela_atualiza, atributos_add, valores_add)
                    

                atributos_aux = []
                atualizacoes = []
                
            
            BD.close()
            

            #Volta para a página dos autores
            return HttpResponseRedirect('/autor/{0}'.format(autor_id))

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = AutorForm(acao='editar', id=autor_id)

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

#Informações de uma editora específica
def autor_detail(request, autor_id): 
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')
           
    if autor_id is None:
        return autor_list(request)

    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Autor"

    atributos = []
    atributos.append(['id_autor as id', 'nome', 'data_nascimento', 'data_falecimento', 'nacionalidade', 'biografia'])

    condicao = "id_autor = %s" % autor_id
    
    join_ = []
    join_.append('')

    tabelas = ["autores"]

    i = 0
    for nome_tabela in tabelas:
        retorno[nome_tabela] =  BD.select(tabela, atributos[i], where=condicao, join=join_[i])
        i += 1

    BD.close()

    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/autor_informacoes.html', retorno)