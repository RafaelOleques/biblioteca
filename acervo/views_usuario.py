from django.http import HttpResponseRedirect
from django.shortcuts import render
from .classes.conexao_BD import ConexaoBD
from .usuarioForm import *

titulo_pagina = "Página do Usuário"
linkTitulo   = "usuario_login"

def usuario_login(request):
    usuario = "postgres"
    senha = "#Fantasma10"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Usuario"

    acao = "Login do {0}".format(tabela)

    if request.method == 'POST':
        #Cria uma instância de form e adiciona nele as informações do request
        form = UsuarioLoginForm(request.POST)

        if form.is_valid():
            request.session['id_usuario'] = form.cleaned_data['id_usuario']

            return HttpResponseRedirect('/acervo/')
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
    senha = "#Fantasma10"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    tabela = "Usuario"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)
    usuarios = BD.select("Usuario", ["codigo", "nome"], nome_atributo=False)
    print(usuarios)

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

            todos_usuarios = BD.select(tabela, "*")
            for usuario in todos_usuarios:
                print("USUARIO:::::", usuario)

            atributos_aux = []
            valores = []

            BD.close()
            

            #Volta para a página dos livros
            return HttpResponseRedirect('/acervo/')

    #Se for um GET ou outro método, então cria um formulário em branco
    else:
        form = UsuarioForm(acao='adicionar')

    retorno['form'] = form  
    retorno['titulo'] = titulo_pagina
    retorno['acao'] = acao
    retorno["linkTitulo"] = linkTitulo
    retorno["add"] = "add_" + "Obra"

    return render(request, 'acervo/add.html', retorno)
