from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .exemplarForms import ExemplarForm
from datetime import date

titulo_pagina = "Livros do Acervo"
linkTitulo   = "obra_list"

def exemplar_reserva(request, obra_id, sequencia):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    tabela = "Exemplar"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    tabela = "Emprestimo_Corrente"

    atributos = ["id_obra", "sequencia", "codigo_usuario", "data_emprestimo", "data_devolucao"]

    data_atual = date.today()
    proxima_data = date.fromordinal(data_atual.toordinal()+7)

    data_emprestimo = data_atual.strftime('%d/%m/%Y')
    data_devolucao = proxima_data.strftime('%d/%m/%Y')

    valores = [obra_id, sequencia, request.session['id_usuario'], data_emprestimo, data_devolucao]

    BD.insert(tabela, atributos, valores)

    inf = BD.select(tabela, atributos)

    BD.close()

    return HttpResponseRedirect('/acervo/obra/{0}'.format(obra_id))

def exemplar_devolucao(request, obra_id, sequencia):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    tabela = "Exemplar"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Pega as informações do empréstimo corrente para adicionar no histórico
    tabela = "Emprestimo_Corrente"
    atributos = ["id_obra", "sequencia", "codigo_usuario", "data_emprestimo", "data_devolucao"]
    condicao = "id_obra = {0} AND sequencia = {1}".format(obra_id, sequencia)

    emprestimo_corrente = BD.select(tabela, atributos, where=condicao)
    emprestimo_corrente = emprestimo_corrente[0]

    print("Emprestimo corrente:::::::::", emprestimo_corrente)

    data_atual = date.today()
    data_devolucao_efetiva = data_atual.strftime('%d/%m/%Y')

    #Deleta o empréstimo corrente
    print("Delete:::::::::::::", tabela, condicao)
    BD.delete(tabela, condicao)

    #Pega as informações para a

    tabela = "Emprestimo_Historico"
    atributos = ["id_obra", "sequencia", "codigo_usuario", "data_emprestimo", "data_devolucao_prevista", "data_devolucao_efetiva"]
    
    valores = [obra_id, sequencia, request.session['id_usuario'], emprestimo_corrente["data_emprestimo"], emprestimo_corrente["data_devolucao"], data_devolucao_efetiva]

    BD.insert(tabela, atributos, valores)

    BD.close()

    return HttpResponseRedirect('/usuario/')



    

def exemplar_add(request, obra_id):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')
        
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Exemplar"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)
    tabela_titulo = "Obra"
    atributo_titulo = ["titulo"]
    condicao_titulo = "id_obra = {0}".format(obra_id)

    informacoes = BD.select(tabela=tabela_titulo, atributos=atributo_titulo, where=condicao_titulo)
    titulo = informacoes[0]["titulo"]

    acao = "Novo {0} de {1}".format(tabela, titulo)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = ExemplarForm(request.POST, acao='adicionar', id=obra_id)

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

            print("Atributos:", atributo_)

            #Pega as informações do Exemplar para add no BD
            for atributo in atributos_aux:
                if atributo in form.cleaned_data:
                    if type(form.cleaned_data[atributo]) is list:
                        for lista in form.cleaned_data[atributo]:
                            valores.append(lista)
                    else:
                        valores.append(form.cleaned_data[atributo])
                else:
                    print("Atributos:", atributo)

                    atributo_.remove(atributo)
            
            #Insere o novo obra no BD
            #ID do último exemplar adicionado
            ultimo_add = BD.ultimo_adicionado("Exemplar", "sequencia") + 1
            
            #Insere o novo exemplar no BD
            atributo_.append("id_obra")
            valores.append(obra_id)
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            BD.close()
            

            #Volta para a página dos livros
            return HttpResponseRedirect('/acervo/obra/{0}'.format(obra_id))

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = ExemplarForm(acao='adicionar', id=obra_id)

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = "add_" + "Obra"

    return render(request, 'acervo/add.html', retorno)
