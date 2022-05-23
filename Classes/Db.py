import psycopg2

class Db:
    def __init__(self, dbname:str, user:str, password:str, host:str):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()