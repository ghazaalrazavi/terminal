import psycopg

class MyContextManager:
    def __init__(self,dsn):
        self.dsn = dsn
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = psycopg.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def __exit__(self,exc_type,exc_val,exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        self.cursor.close()