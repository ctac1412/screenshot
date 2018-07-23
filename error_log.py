import postgresql


def errorLog(module_name,error_message):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    insert = db.prepare("insert into error_log (module_name,error_message) values($1,$2)")
    insert(module_name, str(error_message))