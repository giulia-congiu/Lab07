from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_umidita_media(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """SELECT s.Localita,AVG(s.Umidita)
                       FROM situazione s
                       Where MONTH(s.Data) = %s
                       Group by s.Localita"""
            #quella query mi rida 3 righe fatte così:
            #  citta ----  umidità media per mese selezionato
            cursor.execute(query, (mese,))
            result = cursor.fetchall()
            #se avessi dictionary=True avrei una lista di dizionari [{Località: Torino, umidità: 89}, {...}]:
            #così ho una lista di tuple [(torino, 55), (Genova, 80), (milano, 100)]
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_situazioni_meta_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                       FROM situazione s
                       Where MONTH(s.Data) = %s AND DAY(s.Data) <= 15
                       ORDER BY s.Data ASC"""
            #ottengo una tabella: località -- data -- umidità
            #ordiata per data crescente prendendo i primi 15 gg del mese selezionato
            '''Localita|   Data   |Umidita|
                --------+----------+-------+
                Genova  |2013-03-01|     59|
                Torino  |2013-03-01|     73|
                Milano  |2013-03-01|     80|
                Torino  |2013-03-02|     78|
                Milano  |2013-03-02|     78|
                Genova  |2013-03-02|     46|
                Milano  |2013-03-03|     83|'''
            cursor.execute(query, (mese,))
            for row in cursor: #row è un dizionario !
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
                #in questo modo ottengo direttamente una lista di situazioni
            cursor.close()
            cnx.close()
        return result










    #c'era già ma nn lo uso poi
    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

