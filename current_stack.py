import db_conf
import postgresql


def searchCurrentStack(screen_area):
    return 0

#Получаем номер области экрана, на которой нужно искать элемент для текущего стола
def getStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select stack_area from screen_coordinates where screen_area = " + screen_area)
    return data[0]['stack_area']