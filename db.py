import pymysql as sql


class Database():
    conn = None
    cursor = None

    def __init__(self):
        """
        The constructor initializes the database connection and the cursor
        """
        try:
            self.conn = sql.connect("localhost", "root", "root", "tcgplace")
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise Exception('No database connection. Err: {}'.format(e))

    def close(self):
        """
        Closes the database connection
        """
        self.conn.close()

    def get_by_expansion_id(self, expansion_id=None):
        """
        Get all the cards with the expansion_id passed by param
        :param expansion_id: List of expansion ids or single expansion id to search in database
        :return data: Database search result in Json
        :return count: Number of rows
        """
        if not self.cursor:
            raise Exception('No database connection')
        if type(expansion_id) == list:
            aux = ', '.join(str(id) for id in expansion_id)
            expansion_id = aux
        self.cursor.execute("SELECT * FROM magiccard WHERE expansionId IN ({})".format(expansion_id))
        data = [dict((self.cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in self.cursor.fetchall()]
        count = self.cursor.rowcount
        return data, count

    def is_valid_expansion(self, expansion_id=None):
        """
        Check if the expansion_id param exists in database
        :param expansion_id: The expansion id to search in database
        :return Expansion Name if exists else None
        """
        if not self.cursor:
            raise Exception('No database connection')
        self.cursor.execute("SELECT Name FROM magicexpansion where ExpansionId={}".format(expansion_id))
        data = self.cursor.fetchone()
        return data[0] if data else data

    def get_expansion_ids(self):
        """
        Get all the expansion ids in database
        :return List containing all the expansion ids
        """
        if not self.cursor:
            raise Exception('No database connection')
        self.cursor.execute("SELECT ExpansionId FROM magicexpansion")
        return [ids[0] for ids in self.cursor.fetchall()]
