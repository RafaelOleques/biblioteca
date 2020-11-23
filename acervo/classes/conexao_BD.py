import psycopg2
from .funcoes_auxiliares import *

class ConexaoBD:
    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password 
        #sslmode = "require"

        conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
        self.conn = psycopg2.connect(conn_string) 

        self.cursor = self.conn.cursor()

    #Recebe o tipo de select (opcional), nome da tabela, uma lista com o nome dos atributos
    #a declaração de um join (opcional), uma condição para o where (opcional) 
    #e outras operações desejadas (opcional)
    def _select(self, tabela, atributos, tipo_select="", join=None, where=None, group_by=None, having=None, subconsulta=None):
        try:
            operacoes = ""

            #Verifica se há condição
            operacoes = " " + (join if join else "") + " " + (" WHERE "+where if where else "")

            #Converte a lista em uma string com os atributos separados por virgula
            atributos = str(atributos).strip('[]').replace("'", "")
            
            #Realiza a consulta
            self.cursor.execute("SELECT %s %s FROM %s %s;" % (tipo_select, atributos, tabela, operacoes))
            rows = self.cursor.fetchall()

            return rows
        except:
            return None

    #Retorna o método _select formatado
    # 1. Caso nome_atributo seja verdadeiro, retorna uma lista com as tuplas em forma de dicionário, 
    #    com o nome do seu atributo como chave
    #    -> Deve-se notar que o método não retornará o nome dos atributos no caso que se tenha
    #       um select com * e um join
    # 2. Caso contrário, retorna uma lista com as tuplas
    def select(self, tabela, atributos, tipo_select="", join=None, where=None, group_by=None, having=None, subconsulta=None, nome_atributo=True):
        tuplas = self._select(tabela, atributos, tipo_select, join, where)

        if atributos == "*" and join is None:
            atributos = self.atributos_nome(tabela)
        
        select_result = []

        if nome_atributo and atributos != "*":
            atributos = valida_lista(atributos)

            for tupla in tuplas:
                dict_aux = {}
                i = 0

                for atributo in atributos:
                    atributo = renomeia_atributo(atributo)
                    if 'id_' in atributo:
                        dict_aux[atributo] = int(tupla[i])
                    else:
                        dict_aux[atributo] = tupla[i]
                    i += 1

                select_result.append(dict_aux)
        else:
            return tuplas

        return select_result

    def ultimo_adicionado(self, tabela, id_tabela):
        ultimo = self._select(tabela, "MAX(%s)" % id_tabela)

        return ultimo[0][0]

    #Retorna o nome dos atributos de uma tabela
    def atributos_nome(self, tabela):
        atributos = self._select("pg_attribute", "attname", where="attrelid = '%s'::regclass AND attnum > 0 AND NOT attisdropped;" % tabela)
        resultado = []

        for atributo in atributos:
            resultado.append(atributo[0]) 

        return resultado
        
    #Recebe o nome da tabela, os atributos em forma de lista e os valores em forma de lista
    def insert(self, tabela, atributos, valores):
        try:
            atributos = valida_lista(atributos)
            atributos = formata_lista_string(atributos)
    
            valores = valida_lista(valores)
            valores = formata_lista_string(valores, aspas=True)
            valores = verifica_atributo_numero(atributos, valores)
            operacao  = """INSERT INTO %s (%s) 
            VALUES(%s);""" % (tabela, atributos, valores)
            self.cursor.execute(operacao)
            self.conn.commit()

            return True
        except:
            return False

    #Recebe o nome da tabela e a condição em forma de string
    def delete(self, tabela, condicao):
        try:
            operacao  =  "DELETE FROM %s " % tabela
            operacao +=  "WHERE %s"        % condicao

            self.cursor.execute(operacao)
            self.conn.commit()

            return True
        except:
            return False

    #Recebe o nome da tabela, atualização em forma de string e a condição em forma de string
    def update(self, tabela, atualizacao, condicao):
        try:
                        
            operacoes  = "UPDATE %s " % tabela
            operacoes += "SET %s "    % atualizacao
            operacoes += "WHERE %s"   % condicao

            self.cursor.execute(operacoes)
            self.conn.commit()

            return True
        except:
            return False

    #Encerra o BD
    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    usuario = "postgres"
    senha = "admin123"

    retorno = {} #Variável que armazena informações para serem escritas no HTML
    titulo = "Lista de Livros"
    tabela = "Obra"

    BD = ConexaoBD("localhost", "SistemaBiblioteca", usuario, senha)

    atributos = ['isbn', 'titulo', 'ano_publicacao', 'id_editora']
    #atributos = ['isbn as obra_isbn', 'titulo as obra_titulo', 'ano_publicacao', 'Autor.nome as autor_name', 'Genero.nome as genero_nome', 'Palavras_Chaves.nome as palavra_chave_nome', 'Editora.nome as editora_nome' ]

    condicao = "titulo = 'Linguagens Formais e Automatos'"
    
    join_ =   "JOIN Editora USING (id_editora)"
    join_ +=  "JOIN Autoria USING(id_obra)"
    join_ +=  "JOIN Autor USING(id_autor)"
    join_ +=  "JOIN Classificacao USING(id_obra)"
    join_ +=  "JOIN Genero USING (id_genero)"
    join_ += "JOIN Assunto USING(id_obra)"
    join_ += "JOIN Palavras_Chaves USING (id_palavra_chave)"

    #BD.insert("Genero", "nome", "mamiferos")
    #BD.insert("Classificacao", ['id_obra', 'id_genero'], [2, 4])

    tabela = 'Obra'
    condicao = "titulo = 'Habitos dos mamiferos aquaticos'"
    join_ = "JOIN Assunto USING(id_obra)" + "JOIN Palavras_Chaves USING (id_palavra_chave)"

    valores = ['88888', 'Fantasma da Opera', '15/10/2015', 2]
    #BD.insert(tabela, atributos,valores)
    #informacoes = BD.select(tabela, atributos)
    
    #informacoes = BD.select(tabela, atributos, where=condicao)
    #BD.select("Editora", ["id_editora", "nome"], nome_atributo=False)
    #print(informacoes)

    #print(BD.ultimo_adicionado("Obra", "id_obra"))

    BD.close()

