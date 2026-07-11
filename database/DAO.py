from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting

class DAO():

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    # PUNTO 1a ----------------------------------------------------------
    # Permettere all’utente di scegliere da un menù a tendina un anno tra tutti i possibili anni in cui
    # ci sono stati avvistamenti (ordinati in senso DECRESCENTE).
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as anno
                        from sighting s 
                        order by anno desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])
            cursor.close()
            cnx.close()
        return result
    # FINE PUNTO 1a ------------------------------------------------------

    # PUNTO 1c ----------------------------------------------------------
    # Popolare il menù a tendina Forma con tutte le possibili forme, prese dalla colonna “shape” del db,
    # relative agli avvistamenti nell’anno considerato (escludendo i casi in cui non è specificata nessuna
    # forma, ordinati alfabeticamente).
    @staticmethod
    def getShapesYear(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as forma
                        from sighting s 
                        where year(s.`datetime`) = %s
                        order by s.shape asc"""
            cursor.execute(query, (anno,))

            for row in cursor:
                if row["forma"] != "":
                    result.append(row["forma"])

            cursor.close()
            cnx.close()
        return result
    # FINE PUNTO 1b ------------------------------------------------------

    # PUNTO 1c ----------------------------------------------------------
    # vertici siano tutti gli avvistamenti presenti nella tabella “sighting” che siano avvenuti
    # nell’anno selezionato dall’utente e con la shape desiderata.
    @staticmethod
    def getAllNodes(anno, shape):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    order by s.`datetime` asc"""
            cursor.execute(query, (anno, shape,))

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result

    # un arco fra due avvistamenti esiste se e solo se tali avvistamenti sono avvenuti nello stesso stato.
    # L’arco è uscente dall’avvistamento che è avvenuto temporalmente prima ed entrante nell’avvistamento
    # avvenuto dopo.
    @staticmethod
    def getAllEdges(anno, shape):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select  t1.id as id1, t1.datetime as d1, t2.id as id2, t2.datetime as d2 
                    from (select * from sighting s where s.shape = %s and year(s.`datetime`) = %s) t1, 
                    (select * from sighting s where s.shape = %s and year(s.`datetime`) = %s) t2 
                    where t1.state = t2.state
                    and t1.datetime < t2.datetime"""
            cursor.execute(query, (shape, anno, shape, anno))

            for row in cursor:
                result.append((row["id1"], row["id2"]))

            cursor.close()
            cnx.close()
        return result
    # FINE PUNTO 1c ------------------------------------------------------















