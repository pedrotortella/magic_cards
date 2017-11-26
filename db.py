import pymysql as sql


class Database():
    conn = None
    cursor = None

    def __init__(self):
        try:
            self.conn = sql.connect("localhost", "root", "root", "tcgplace")
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise Exception('No database connection. Err: {}'.format(e))

    def close(self):
        self.conn.close()

    def get_by_expansion_id(self, expansion_id=None):
        if not self.cursor:
            raise Exception('No database connection')
        self.cursor.execute("SELECT * FROM magiccard WHERE expansionId = {}".format(expansion_id))
        data = [dict((self.cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in self.cursor.fetchall()]
        count = self.cursor.rowcount
        return data, count

    def is_valid_expansion(self, expansion_id=None):
        if not self.cursor:
            raise Exception('No database connection')
        self.cursor.execute("SELECT Name FROM magicexpansion where ExpansionId={}".format(expansion_id))
        data = self.cursor.fetchone()
        return data[0] if data else data

    def get_expansion_ids(self):
        if not self.cursor:
            raise Exception('No database connection')
        self.cursor.execute("SELECT ExpansionId FROM magicexpansion")
        return [ids[0] for ids in self.cursor.fetchall()]
