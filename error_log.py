import postgresql
import db_conf

def errorLog(module_name,error_message):
    db = postgresql.open(db_conf.connectionString())
    insert = db.prepare("insert into error_log (module_name,error_message) values($1,$2)")
    insert(module_name, str(error_message))