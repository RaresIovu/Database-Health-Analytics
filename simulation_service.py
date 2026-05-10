from database.db import get_connection

def getAllKnowledge():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT id, name, quantity FROM objects")
            rows = cur.fetchall()
            content = []
            for row in rows:
                object = {
                    "id": row[0],
                    "name": row[1],
                    "quantity": row[2]
                }
                content.append(object)
            return content
        
def addKnowledge(name, quantity):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("INSERT INTO objects (name, quantity) VALUES (%s, %s)", (name, quantity))