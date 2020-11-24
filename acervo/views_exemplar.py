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

            atributo_.append("id_obra")
            valores.append(obra_id)
            
            #Insere o novo obra no BD
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
'''
def obra_delete(request, obra_id):
    usuario = "postgres"
    senha = "admin123"

    tabela = "Obra"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    retorno["titulo"] = "Not Found - Retorne ao Acervo"
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    condicao = "id_obra = %s" % obra_id
    
    BD.delete(tabela, condicao)

    return HttpResponseRedirect('/acervo/')


def obra_edit(request, obra_id):    
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"
    acao = "Edição - "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = ObraForm(request.POST, acao='editar', id=obra_id)

        if form.is_valid():
            tabelas = ["Autor", "Genero", "Palavras_Chaves"]
            tabelas_n = ['Autoria', 'Classificacao', 'Assunto']
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
            
            #Dicionário para saber qual tabela está ligando a primeira com Obra
            tabela_relacoes = {
                "Autor"           : "Autoria",
                "Genero"          : "Classificacao" ,
                "Palavras_Chaves" : "Assunto",
                }
            
            #Dicionário para saber qual é o id de cada tabela
            id_obra = "id_obra"

            #Informações do Exemplar
            tabela = "Obra"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            atualizacoes = []

            #Pega as informações do Exemplar para add no BD
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
            condicao = "{0} = {1}".format(id_obra, obra_id)

            #Atualiza a obra
            BD.update(tabela, atualizacoes, condicao)


            atributos_aux = []
            atualizacoes = []

            #Pega os valores e atributos dos demais que fazem relação com obra
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

                    condicao = "{0} = {1}".format(id_obra, obra_id)
                    BD.delete(tabela_atualiza, condicao)

                #Adiciona as novas relações
                for valor in atualizacoes:
                    tabela_atualiza = tabela_relacoes[tabela]

                    atributos_add = [id_obra, atributos_aux[0]]
                    valores_add = [obra_id, valor]
                    BD.insert(tabela_atualiza, atributos_add, valores_add)
                    

                atributos_aux = []
                atualizacoes = []


            BD.close()
            
            #Volta para a página dos livros
            return HttpResponseRedirect('/acervo/obra/{0}'.format(obra_id))

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        #return render(request, 'acervo/add.html', retorno)
        form = ObraForm(acao='editar', id=obra_id)

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)
'''