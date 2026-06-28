import sqlite3

class Database():
    def __init__(self, name):
        self.name = name
        self.conn = None

    def start(self):
        self.conn = sqlite3.connect(self.name)
        return self.conn
    
    def end(self):
        if self.conn:
            self.conn.close()
            self.conn = None