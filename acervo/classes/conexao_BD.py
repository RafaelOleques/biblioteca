import psycopg2

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
    def _select(self, tabela, atributos, tipo_select="", join=None, condicao=None, outra_operacao=None):
        try:
            operacoes = ""

            #Verifica se há condição
            operacoes =  (join if join else "") + (" WHERE "+condicao if condicao else "") + (outra_operacao if outra_operacao else "")

            #Converte a lista em uma string com os atributos separados por virgula
            atributos = str(atributos).strip('[]').replace("'", "")

            #Realiza a consulta
            self.cursor.execute("SELECT %s %s FROM %s %s;" % (tipo_select, atributos, tabela, operacoes))
            rows = self.cursor.fetchall()

            return rows
        except:
            return None
        
    #Recebe o nome da tabela, os atributos em forma de lista e os valores em forma de lista
    def insert(self, tabela, atributos, valores):
        try:
            tabela = str(tabela)
            atributos = str(atributos).strip("[]").replace("'", "")
            valores = str(valores).strip("[]")

            self.cursor.execute("""
                                INSERT INTO %s (%s) 
                                VALUES(%s)
                                """ % (tabela, atributos, valores))
            self.conn.commit()

            return True
        except:
            return False

    #Recebe o nome da tabela e a condição em forma de string
    def delete(self, tabela, condicao):
        try:
            self.cursor.execute("""
                                DELETE FROM %s
                                WHERE %s
                                """ % (tabela, condicao))
            self.conn.commit()

            return True
        except:
            return False

    #Recebe o nome da tabela, atualização em forma de string e a condição em forma de string
    def update(self, tabela, atualizacao, condicao):
        try:
            self.cursor.execute("""
                                UPDATE %s
                                SET %s
                                WHERE %s
                                """ % (tabela, atualizacao, condicao))
            self.conn.commit()

            return True
        except:
            return False

    #Retorna o nome dos atributos de uma tabela
    def atributos_nome(self, tabela):
        atributos = self._select("pg_attribute", "attname", condicao="attrelid = '%s'::regclass AND attnum > 0 AND NOT attisdropped;" % tabela)
        resultado = []

        for atributo in atributos:
            resultado.append(atributo[0]) 

        return resultado

    #Retorna o método _select formatado
    # 1. Caso nome_atributo seja verdadeiro, retorna uma lista com as tuplas em forma de dicionário, 
    #    com o nome do seu atributo como chave
    # 2. Caso contrário, retorna uma lista com as tuplas
    def select(self, tabela, atributos, tipo_select="", join=None, condicao=None, outra_operacao=None, nome_atributo=True):
        tuplas = self._select(tabela, atributos, tipo_select, join, condicao, outra_operacao)
        if atributos == "*":
            atributos = self.atributos_nome(tabela)
        select_result = []

        if nome_atributo:
            for tupla in tuplas:
                dict_aux = {}
                i = 0

                for atributo in atributos:
                    dict_aux[atributo] = tupla[i]
                    i += 1

                select_result.append(dict_aux)
        else:
            return tuplas

        return select_result

    #Encerra o BD
    def close(self):
        # Cleanup
        self.cursor.close()
        self.conn.close()
