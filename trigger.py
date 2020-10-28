from connection import DBConnect


class Trigger:
    def __init__(self, connect):
        self.connect = connect

    def create_table(self):
        cursor = self.connect.cursor()
        try:
            cursor.execute("""create table old_record(id SERIAL,
                                customer_name varchar(50),
                                customer_id int,
                                action varchar(50),
                                primary key(id))""")
            self.connect.commit()
            return {"message": "create data successfully", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}

    def create_trigger(self):
        cursor = self.connect.cursor()
        try:
            cursor.execute("""create or replace function log_change()
                            returns trigger as 
                            $BODY$
                            begin
                            insert into old_record(customer_name,customer_id,action)
                            values(old.name,old.id,TG_ARGV[0]);
                            return new;
                            end;
                            $BODY$
                            language plpgsql;""")
            self.connect.commit()
            return {"message": "create trigger successfully", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}
    def customer_trigger(self):
        cursor = self.connect.cursor()
        try:
            cursor.execute("""create trigger insert_customer after insert
                                on customer for each row
                                execute procedure log_change('insert')""")
            cursor.execute("""create trigger update_customer after update
                                on customer for each row
                                execute procedure log_change('update')""")
            cursor.execute("""create trigger delete_customer after delete
                                on customer for each row
                                execute procedure log_change('delete')""")
            self.connect.commit()
            return {"message": "create trigger successfully", "status": True}
        except Exception as e:
            return {"message": "there is an error", "status": False, "error": str(e)}
con = DBConnect(username="hla", password="password", port="5432", host="localhost", database="postgres")
connect = con.connect()
t = Trigger(connect=connect['connect'])
print(t.customer_trigger())
