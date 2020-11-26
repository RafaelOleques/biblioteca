def isNumber(valor):
        if type(valor) is not str:
            return True

#Valida se é uma lista, caso não seja retorna em forma de lista
def valida_lista(entrada):
    if type(entrada) is not list:
        entrada = [entrada, ]
    
    return entrada
    

#Quando tiver um as, renomeia o atributo para o que vem depois
def renomeia_atributo(atributo):
    NOVO_NOME = 1
    comando = ' as '
    novo_atributo = atributo

    if comando in atributo:
        novo_atributo = novo_atributo.split(comando)
        novo_atributo = novo_atributo[NOVO_NOME]
    
    return novo_atributo

#Verifica se há um atributo que deveria ser um número, se sim, converte para int
def verifica_atributo_numero(atributos, valores):
    i = 0
    valores_ = valores.split(', ')
    atributos_ = atributos.split(', ')
    val = []
    for atributo in atributos_:
        if "id_" in atributo or "edicao" in atributo:
            val.append(int(valores_[i].replace("'", "")))
        else:
            val.append(valores_[i].replace("'", ""))
        i += 1    

    return str(val).strip('[]')


#Formata uma lista para uma string com os elementos separados por virgula
#Os elementos podem ou não estarem entre aspas simples
def formata_lista_string(lista, aspas=False):
    text = ''

    if aspas:
        base_string = "'%s', "
    else:
        base_string = "%s, "

    base_not_string = "%s, "

    for atributo in lista:
        if isNumber(atributo):
            text += base_not_string % atributo
        else:
            text += base_string % atributo

    return text[:-2]

