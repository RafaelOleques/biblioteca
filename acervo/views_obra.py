from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .obraForms import Add_ObraForm
import datetime

titulo_pagina = "Livros do Acervo"
linkTitulo   = "obra_list"

def formata_data_BD(data):
    nova_data = data.split('/')
    return "datetime.date(%s, %s, %s)" % nova_data[0], nova_data[1], nova_data[2]

def obra_redirect(request):
    retorno = {}
    retorno["titulo"] = "Not Found - Retorne ao Acervo"
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_Obra'
    return render(request, 'acervo/obra_list.html', retorno)

def obra_list(request):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['id_obra as id', 'isbn', 'titulo', 'ano_publicacao']

    informacoes = BD.select(tabela, atributos)

    retorno["obras"] = informacoes
    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela
    BD.close()

    return render(request, 'acervo/obra_list.html', retorno)

def obra_add(request):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"
    acao = "Nova "+ tabela
    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = Add_ObraForm(request.POST)

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
        form = Add_ObraForm()

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/add.html', retorno)

def obra_detail(request, obra_id):    
    if obra_id is None:
        return obra_list(request)

    usuario = "postgres"
    senha = "admin123"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Obra"

    atributos = []
    atributos.append(['id_obra', 'isbn', 'titulo', 'ano_publicacao'])
    atributos.append('Autor.nome as nome')
    atributos.append('Genero.nome as nome')
    atributos.append('Palavras_Chaves.nome as nome')
    atributos.append('Editora.nome as nome')

    condicao = "id_obra = %s" % obra_id
    
    join_ = []
    join_.append('')
    join_.append("JOIN Autoria USING(id_obra) " + "JOIN Autor USING(id_autor)")
    join_.append("JOIN Classificacao USING(id_obra) " + "JOIN Genero USING (id_genero)")
    join_.append("JOIN Assunto USING(id_obra)" + "JOIN Palavras_Chaves USING (id_palavra_chave)")
    join_.append("JOIN Editora USING (id_editora)")

    tabelas = ["obras", "autores", "generos", "palavras_chaves", "editoras"]

    i = 0
    for nome_tabela in tabelas:
        retorno[nome_tabela] =  BD.select(tabela, atributos[i], where=condicao, join=join_[i])
        i += 1

    BD.close()

    retorno["titulo"] = titulo_pagina
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = 'add_' + tabela

    return render(request, 'acervo/obra_informacoes.html', retorno)