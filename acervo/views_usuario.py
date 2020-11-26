from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .usuarioForm import *

titulo_pagina = "Página do Usuário"
linkTitulo   = "usuario_detail"

def usuario_login(request):
    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Usuario"

    acao = "Login do {0}".format(tabela)

    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = UsuarioLoginForm(request.POST)

        if form.is_valid():
            request.session['id_usuario'] = form.cleaned_data['id_usuario']
            
            #Tipo de usuário

            usuario = "postgres"
            senha = "admin123"

            retorno = {} #Variável que armazena informações para serem escritas no HTML
            tabela = "Usuario"

            BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

            #Administrador?
            tabela = "Usuario"
            atributos = ["codigo"]
            condicao = "codigo = {0}".format(request.session['id_usuario'])
            join = "JOIN Administrador USING(codigo)"

            Administrador = BD.select(tabela, atributos, where=condicao, join=join)

            #Bibliotecário?
            tabela = "Usuario"
            atributos = ["codigo"]
            condicao = "codigo = {0}".format(request.session['id_usuario'])
            join = "JOIN Bibliotecario USING(codigo)"

            bibliotecario = BD.select(tabela, atributos, where=condicao, join=join)

            if Administrador != []:
                request.session['tipo_usuario'] = "Administrador"
            elif bibliotecario != []:
                request.session['tipo_usuario'] = "Bibliotecário"
            else:
                request.session['tipo_usuario'] = "Usuário comum"

            return HttpResponseRedirect('/usuario/')
    else:
        form = UsuarioLoginForm()

    request.session['usuario'] = "postgres"

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = "usuario_add"

    return render(request, 'acervo/add.html', retorno)



def usuario_add(request):
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Usuario"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)
    usuarios = BD.select("Usuario", ["codigo", "nome"], nome_atributo=False)

    acao = "Novo {0}".format(tabela)

    #Verifica se é um POST para processar os dados
    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = UsuarioForm(request.POST, acao='adicionar')

        if form.is_valid():
            #Salva os atributos em uma variável auxiliar para que possa excluir dentro do for 
            #os que não vão ser utilizados

            #Identifica os valores dos atributos que foram recebidos
            i = 0
            atributos_aux = []

            #Informações do Usuario
            tabela = "Usuario"
            atributo_ = BD.atributos_nome(tabela)
            atributos_aux.extend(atributo_)
            valores = []

            #Pega as informações do Usuario para add no BD
            for atributo in atributos_aux:
                if atributo in form.cleaned_data and "id_" not in atributo:
                    if type(form.cleaned_data[atributo]) is list:
                        for lista in form.cleaned_data[atributo]:
                            valores.append(lista)
                    else:
                        valores.append(form.cleaned_data[atributo])
                else:
                    atributo_.remove(atributo)
            
            #Insere o novo Usuario no BD
            print(tabela, atributo_, valores)
            BD.insert(tabela, atributo_, valores)

            atributos_aux = []
            valores = []

            BD.close()
            

            #Volta para a página dos livros
            return HttpResponseRedirect('/login/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = UsuarioForm(acao='adicionar')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = "add_" + "Obra"

    return render(request, 'acervo/add.html', retorno)
    
def usuario_detail(request):
    if 'id_usuario' not in request.session:
        return HttpResponseRedirect('/login/')

    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Usuario"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    #Mensagem da página do usuário
    atributos = "nome"
    condicao = "codigo = {0}".format(request.session['id_usuario'])
    print(tabela, atributos, condicao)
    nome_usuario = BD.select(tabela, atributos, where=condicao)

    acao = "Bem-vindo, {0}!".format(nome_usuario[0]["nome"])

    #Tipo de usuário

    tipo_usuario = request.session['tipo_usuario']

    #Empréstimos corrente
    tabela = "Emprestimo_Corrente"
    atributos = ["Obra.id_obra as id", "sequencia", "titulo", "edicao", "data_emprestimo", "data_devolucao"]
    condicao = "codigo_usuario = {0}".format(request.session['id_usuario'])

    join  = "JOIN Usuario ON Emprestimo_Corrente.codigo_usuario = Usuario.codigo "
    join += "JOIN Obra USING(id_obra) "
    join += "JOIN Exemplar USING(sequencia)"

    informacoes = BD.select(tabela, atributos, where=condicao, join=join)
    emprestimos_corrente = informacoes

    #Histórico de empréstimos
    tabela = "Emprestimo_Historico"
    atributos = "count(id_obra) as nro_historico"
    condicao = "codigo_usuario = {0}".format(request.session['id_usuario'])
    group_by = "codigo_usuario"

    informacoes = BD.select(tabela, atributos, where=condicao, group_by=group_by)

    if informacoes == []:
        total_livros_historico = 0
    else:
        total_livros_historico = informacoes[0]["nro_historico"]

    #Total de livros com o usuário
    tabela = "Emprestimo_Corrente"
    atributos = "count(id_obra) as nro_emprestimos"
    condicao = "codigo_usuario = {0}".format(request.session['id_usuario'])
    group_by = "codigo_usuario"

    informacoes = BD.select(tabela, atributos, where=condicao, group_by=group_by)

    if informacoes == []:
        total_livros_corrente = 0
    else:
        total_livros_corrente = informacoes[0]["nro_emprestimos"]


    BD.close()
    
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = "add_" + "Obra"
    retorno["total_livros_corrente"] = total_livros_corrente
    retorno["emprestimos_corrente"] = emprestimos_corrente
    retorno["tipo_usuario"] = tipo_usuario
    retorno["total_livros_historico"] = total_livros_historico

    return render(request, 'acervo/usuario_informacoes.html', retorno)