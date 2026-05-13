from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO:

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from airports"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(row(**)))    #SISTEMARE

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.IATA_CODE, count(*) as N
                    from (select a.ID , a.IATA_CODE , f.AIRLINE_ID 
                    from airports a , flights f 
                    where a.ID = f.ORIGIN_AIRPORT_ID  
                    or a.ID  = f.DESTINATION_AIRPORT_ID
                    group by a.ID, a.IATA_CODE , f.AIRLINE_ID) t
                    group by t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMapA[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.origin_airport_id as aeroportoP, f.destination_airport_id as aeroportoA, count(*) as peso
                   from flights f
                   group by f.origin_airport_id, f.destination_airport_id
                   order by f.origin_airport_id, f.destination_airport_id"""

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(idMapA[row["aeroportoP"]],idMapA[row["aeroportoA"]], row["peso"]))

        cursor.close()
        conn.close()
        return result
