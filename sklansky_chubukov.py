import postgresql
import db_conf

def getValidStackValueToPush(hand):
    db = postgresql.open(db_conf.connectionString())
    data = db.query(
        "select stack_value from sklansky_chubukov where hand = " + hand + " order by id desc limit 1")
    return data[0]['stack_value']