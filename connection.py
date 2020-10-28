import psycopg2


class DBConnect:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        try:
            connection = psycopg2.connect(user=self.username, password=self.password, host=self.host, port=self.port,
                                          database=self.database)
            return {"message": "connection successfully", "connect": connection, "status": True}
        except Exception as e:
            return {"message": "not successful", "error": str(e), "status": False}

    def disconnect(self):
        connect = self.connect()
        if connect["status"]:
            connect["connect"].close()
            return {"message": "close successfully", "status": True}
        return {"message": "cant close this session", "status": False, "error": connect["error"]}



