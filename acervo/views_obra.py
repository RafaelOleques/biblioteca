from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .obraForms import *
import datetime

titulo_pagina = "Livros do Acervo"
linkTitulo   = "obra_list"

def formata_data_BD(data):
    nova_data = data.split('/')
    return "datetime.date(%s, %s, %s)" % nova_data[0], nova_data[1], nova_data[2]

#Caso entre em um link inválido
def obra_redirect(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    retorno = {}
    retorno["titulo"] = "Not Found - Retorne ao Acervo"
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_Obra'
    return render(request, 'acervo/obra_list.html', retorno)

#Lista todas as obras
def obra_list(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['id_obra as id', 'isbn', 'titulo', 'ano_publicacao']

    join = ""
    group_by = ""
    having = ""

    if request.method == 'POST':
        atributos.append("COUNT(id_genero)")
        join = " JOIN Classificacao USING(id_obra) "+" JOIN Genero USING (id_genero) "
        group_by = 'id, isbn, titulo, ano_publicacao'
        having = "count(id_genero) > 1 "



    informacoes = BD.select(tabela, atributos, join=join, group_by=group_by, having=having)

    retorno["obras"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    

    BD.close()

    return render(request, 'acervo/obra_list.html', retorno)

def obra_add(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"
    acao = "Adição - "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = ObraForm(request.POST, acao='adicionar', id='2')

        if form.is_valid():
            tabelas = ["Autor", "Genero", "Palavras_Chaves"]
            tabelas_n = ['Autoria', 'Classificacao', 'Assunto']
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
            
            #Dicionário para saber qual tabela está ligando a primeira com Obra
            tabela_id = {
                "Autor"           : "Autoria",
                "Genero"          : "Classificacao" ,
                "Palavras_Chaves" : "Assunto",
                }

            #Informações da Obra
            tabela = "Obra"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações da Obra para add no BD
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

            #ID da última obra adicionada
            ultimo_add = BD.ultimo_adicionado("Obra", "id_obra") + 1
            
            #Insere a nova obra no BD
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            #Pega os valores e atributos dos demais que fazem relação com obra
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
                    atributos_add = ["id_obra", atributos_aux[0]]
                    valores_add = [ultimo_add,valor]

                    BD.insert(tabela_add, atributos_add, valores_add)

                atributos_aux = []
                valores = []

            BD.close()
            

            #Volta para a página dos livros
            return HttpResponseRedirect('/acervo/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = ObraForm(acao='adicionar', id='2')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def obra_delete(request, obra_id):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

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
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

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

            #Informações da Obra
            tabela = "Obra"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            atualizacoes = []

            #Pega as informações da Obra para add no BD
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

#Informações de uma obra específica
def obra_detail(request, obra_id):   
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    if obra_id is None:
        return obra_list(request)

    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"

    #Atributos e joins para cada um dos select
    #Cada posição da lista corresponde a um select
    atributos = []
    join_ = []

    atributos.append(['id_obra as id', 'isbn', 'titulo', 'ano_publicacao'])
    join_.append('')

    atributos.append('Autor.nome as nome')
    join_.append("JOIN Autoria USING(id_obra) " + "JOIN Autor USING(id_autor)")

    atributos.append('Genero.nome as nome')
    join_.append("JOIN Classificacao USING(id_obra) " + "JOIN Genero USING (id_genero)")

    atributos.append('Palavras_Chaves.nome as nome')
    join_.append("JOIN Assunto USING(id_obra)" + "JOIN Palavras_Chaves USING (id_palavra_chave)")

    atributos.append('Editora.nome as nome')
    join_.append("JOIN Editora USING (id_editora)")

    condicao = "id_obra = %s" % obra_id

    #Nome das tabelas que será retornado para a página
    tabelas = ["obras", "autores", "generos", "palavras_chaves", "editoras"]

    i = 0
    #Realização das consultas, salvando o resultado em um dicionário com o indice como
    #o nome da tabela, a qual faz referência
    for nome_tabela in tabelas:
        retorno[nome_tabela] =  BD.select(tabela, atributos[i], where=condicao, join=join_[i])
        i += 1

    #Adiciona os exemplares que não estão reservados
    atributos.append(['sequencia', 'Exemplar.edicao as edicao', 'Sub_Biblioteca.nome as sub_biblioteca'])
    join_.append("JOIN Exemplar USING (id_obra) " + "JOIN Sub_Biblioteca USING (id_subBiblioteca)")
    
    condicao  = "id_obra = {0} ".format(obra_id)
    
    sub_consulta  = "SELECT sequencia FROM Emprestimo_Corrente "
    sub_consulta += "WHERE id_obra = {0}".format(obra_id)

    condicao += " AND sequencia NOT IN ({0})".format(sub_consulta)

    retorno["exemplares_disponiveis"] =  BD.select(tabela, atributos[-1], where=condicao, join=join_[-1])

    #Adiciona os exemplares que estão reservados
    atributos.append(['Exemplar.edicao as edicao', 'Sub_Biblioteca.nome as sub_biblioteca'])
    join_.append("JOIN Exemplar USING (id_obra) " + "JOIN Sub_Biblioteca USING (id_subBiblioteca)")
    
    condicao  = "id_obra = {0} ".format(obra_id)
    
    sub_consulta  = "SELECT sequencia FROM Emprestimo_Corrente "
    sub_consulta += "WHERE id_obra = {0}".format(obra_id)

    condicao += " AND sequencia IN ({0})".format(sub_consulta)
    
    retorno["exemplares_nao_disponiveis"] =  BD.select(tabela, atributos[-1], where=condicao, join=join_[-1])

    
    #Lista as obras que possuem mesmo genero da obra mostrada
    tabela = "Obra"
    atributos.append(['obra.titulo as titulo'])
    join_.append('')        
    
    sub_consulta = "Select distinct c3.id_genero FROM Obra o3 natural join classificacao c3 where o3.id_obra = obra.id_obra"
    condicao = "id_obra <> {0} AND NOT EXISTS (SELECT o2.titulo FROM Obra o2 natural join Classificacao c2 WHERE o2.id_obra = {0} AND c2.id_genero NOT IN ({1}))".format(obra_id, sub_consulta)
    
    retorno["generos_similares"] =  BD.select(tabela, atributos[-1], where=condicao, join=join_[-1])

    BD.close()

    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/obra_informacoes.html', retorno)