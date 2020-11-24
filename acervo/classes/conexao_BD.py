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
    def _select(self, tabela, atributos, tipo_select="", join="", where="", group_by="", having="", order_by="", subconsulta=""):
        try:
            operacoes = ""

            #Verifica se há condição
            #operacoes = " " + (join if join else "") + " " + (" WHERE "+where if where else "")
            where = (" WHERE "+where if where else "")
            group_by = (" GROUP BY "+group_by if group_by != "" else "")

            #Converte a lista em uma string com os atributos separados por virgula
            atributos = str(atributos).strip('[]').replace("'", "")
            
            #Realiza a consulta
            consulta  = "SELECT {0} {1} FROM {2} ".format(atributos, tipo_select, tabela)
            consulta += "{0} ".format(join)
            consulta += "{0} ".format(where)
            consulta += "{0} ".format(group_by)
            consulta += "{0} ".format(having)
            consulta += "{0} ".format(order_by)
  

            #self.cursor.execute("SELECT %s %s FROM %s %s;" % (tipo_select, atributos, tabela, operacoes))
            self.cursor.execute(consulta)
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
    def select(self, tabela, atributos, tipo_select="", join="", where="", group_by="", nome_atributo=True):
        tuplas = self._select(tabela, atributos, tipo_select, join, where, group_by)

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

    atributos = ['titulo', 'edicao', 'sequencia']

    tabela = 'Obra'
    join_ = "JOIN Exemplar USING(id_obra)"

    informacoes = BD.select("Editora", ["id_editora", "nome"], nome_atributo=True)
    print(informacoes)

    #print(BD.ultimo_adicionado("Obra", "id_obra"))

    BD.close()

