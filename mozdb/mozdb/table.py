class Table():
    def __init__(self, db, name):
        self.name = name
        self.db = db

    def create(self, columns):
        cols = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        ql = f"CREATE TABLE IF NOT EXISTS {self.name} (ID INTEGER PRIMARY KEY AUTOINCREMENT, {cols})"
        self.db.conn.cursor().execute(ql)
        self.db.conn.commit()

    def delete(self, name):
        ql = f"DROP TABLE {name};"
        self.db.conn.cursor().execute(ql)
        self.db.conn.commit()

    def delete_column(self, tname, cname):
        ql = f"ALTER TABLE {tname} DROP COLUMN {cname};"
        self.db.conn.cursor().execute(ql)
        self.db.conn.commit()
    
    def rename_column(self, tname, oname, nname):
        ql = f"ALTER TABLE {tname} RENAME {oname} TO {nname};"
        self.db.conn.cursor().execute(ql)
        self.db.conn.commit()

    def insert(self, tname, data):
        keys = ', '.join([cols for cols in data.keys()])
        values = tuple(data.values())
        placeholders = ', '.join(['?' for _ in data])
        ql = f"INSERT INTO {tname} ({keys}) VALUES ({placeholders})"
        self.db.conn.cursor().execute(ql, values)
        self.db.conn.commit()
    
    def find(self, tname, data=None):
        cursor = self.db.conn.cursor()
        if data is None:
            cursor.execute(f"SELECT * FROM {tname}")
        else:
            conditions = ' AND '.join([f"{col} = ?" for col in data.keys()])
            values = tuple(data.values())
            cursor.execute(f"SELECT * FROM {tname} WHERE {conditions}", values)
        return cursor.fetchall()

    def update(self, tname, condition, new_data):
        cursor = self.db.conn.cursor()
        set_clause = ', '.join([f"{col} = ?" for col in new_data.keys()])
        where_clause = ', '.join([f"{col} = ?" for col in condition.keys()])
        values = tuple(new_data.values()) + tuple(condition.values())
        cursor.execute(f"UPDATE {tname} SET {set_clause} WHERE {where_clause}", values)
        self.db.conn.commit()

    def delete(self, tname, data):
        keys = ', '.join([cols for cols in data.keys()])
        values = tuple(data.values())
        placeholders = ', '.join(['?' for _ in data])
        ql = f"DELETE FROM {tname} WHERE {keys} = ({placeholders})"