from connection import DBConnect


class Customer:
    def __init__(self, connect):
        self.connect = connect

    def create_table(self):
        cursor = self.connect.cursor()
        try:
            cursor.execute("""create table customer(id SERIAL,
                                                    name varchar(50) not null,
                                                     email varchar(100) not null UNIQUE,
                                                     phone varchar(10) ,
                                                     about varchar(700),
                                                     primary key(id))""")
            self.connect.commit()
            return {"message": "create data successfully", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}

    def insert_data(self, data):
        cursor = self.connect.cursor()
        try:
            cursor.execute(f"""insert into customer(name,email,phone,about)
                                values('{data["name"]}','{data["email"]}','{data["phone"]}','{data["about"]}')""")
            self.connect.commit()
            return {"message": "insert data successfully ", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}

    def update_data(self, data):
        cursor = self.connect.cursor()
        try:
            cursor.execute(f"""update customer set name='{data["name"]}', email='{data["email"]}',
                                phone='{data["phone"]}',about='{data['about']}'
                                where id={data["id"]}""")
            self.connect.commit()
            return {"message": "update data successfully ", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}

    def delete(self, ids=None, email=None):
        cursor = self.connect.cursor()
        try:
            if ids:
                cursor.execute(f"""delete from customer where id={ids}""")
            elif email:
                cursor.execute(f"""delete from customer where email='{email}'""")
            self.connect.commit()
            return {"message": "delete data successfully ", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}

    def fetch_record(self, email=None):
        cursor = self.connect.cursor()
        try:
            cust = []
            if email:
                cursor.execute(f"""select * from customer where email='{email}'""")
                columns = [desc[0] for desc in cursor.description]
                customer_data = cursor.fetchone()
                return {"message": "list data", "status": True, "data": dict(zip(columns, customer_data))}
            else:
                cursor.execute(f"""select * from customer""")
                customer_data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            for data in customer_data:
                cust.append(dict(zip(columns, data)))
            return {"message": "list data", "status": True, "data": cust}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}


con = DBConnect(username="hla", password="password", port="5432", host="localhost", database="postgres")
connect = con.connect()
customer = Customer(connect=connect['connect'])
print(customer.delete(ids=1))
