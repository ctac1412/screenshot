import error_log


def connection_string():
    return 'pq://postgres:postgres@localhost:5432/postgres'


def get_element_area(screen_area, element, db):
    sql = "select " + element + " from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_element_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates " \
          "where active = 1 and screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def get_bar_area(screen_area, db):
    sql = "select action_btn_area from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_bar_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def get_stack_area(screen_area, db):
    sql = "select stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_opponent_stack_area(screen_area, db):
    sql = "select opponent_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_stack_images(db):
    data = db.query("select trim(image_path) as image_path, stack_value from stack where active = 1 order by id desc")
    return data


def get_stack_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, screen_area)
    return data


def get_opponent_stack_data(screen_area, opponent_area, db):
    sql = "select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area " \
          "from screen_coordinates as sc inner join opponent_screen_coordinates as opp " \
          "on sc.opponent_stack_area = opp.screen_area " \
          "where sc.screen_area = $1 and opp.opponent_area = $2"
    data = db.query(sql, int(screen_area), int(opponent_area))
    return data


def get_allin_stack_area(screen_area, db):
    sql = "select all_in_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_bank_stack_area(screen_area, db):
    sql = "select bank_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_blind_area(screen_area, db):
    sql = "select blind_area from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_blind_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def get_flop_area(screen_area, db):
    sql = "select flop_area from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_flop_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def get_opponent_card_area(screen_area, db):
    sql = "select headsup_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_opponent_card_data(screen_area, db):
    sql = "select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area,opp.opponent_area " \
          "from screen_coordinates as sc " \
          "inner join opponent_screen_coordinates as opp on sc.headsup_area = opp.screen_area " \
          "where sc.screen_area = $1 order by opp.opponent_area"
    data = db.query(sql, int(screen_area))
    return data


def insert_image_path_into_db(image_path, screen_area, db):
    try:
        insert = db.prepare("insert into screenshots (image_path,screen_area) values($1,$2)")
        insert(image_path, int(screen_area))
    except Exception as e:
        print('insertImagePathIntoDb ' + str(e))
        error_log.error_log('insertImagePathIntoDb', str(e))


def get_screen_data(db):
    try:
        data = db.query("select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse "
                        "from screen_coordinates where active = 1 and alias = 'workspace'")
        return data
    except Exception as e:
        error_log.error_log('getScreenData', str(e))


def get_cards(db):
    data = db.query("select trim(image_path) as image_path, trim(alias) as alias from cards")
    return data


def get_allin_stack_images(db):
    data = db.query("select trim(image_path) as image_path, stack_value from all_in_stack order by id desc")
    return data


def get_bank_stack_images(db):
    data = db.query("select trim(image_path) as image_path, stack_value from bank_stack order by id desc")
    return data


def get_actions_buttons(db):
    data = db.query("select trim(image_path) as image_path,trim(opponent_action) as opponent_action, "
                    "trim(alias) as alias from opponent_last_action")
    return data


def get_last_screen(screen_area, db, limit=1):
    sql = "select trim(image_path)as image_path from screenshots where screen_area = $1 order by id desc limit $2"
    data = db.query(sql, int(screen_area), limit)
    return data


def get_current_cards(condition, db):
    sql = "select trim(image_path) as image_path, trim(alias) as alias from cards where alias in ($1)"
    data = db.query.first(sql, condition)
    return data


def get_reaction_to_opponent(hand, position, is_headsup, last_opponent_action, stack, action, db):
    data = db.query("select trim(reaction_to_opponent) as reaction_to_opponent from preflop_chart "
                    "where hand = '" + hand + '\'' + " and position = '" + position + '\'' +
                    " and is_headsup = '" + str(is_headsup) + '\'' + " and opponent_last_action" +
                    last_opponent_action + ' and stack = ' + str(stack) + " and action = '" + action + '\'')
    return data


def get_action_from_preflop_chart(hand, position, is_headsup, last_opponent_action, stack, db):
    data = db.query("select trim(action) as action from preflop_chart "
                    "where hand = '" + hand + '\'' + " and position = '" + position + '\'' +
                    " and is_headsup = '" + str(is_headsup) + '\'' + " and opponent_last_action" +
                    last_opponent_action + " and stack = " + str(stack))
    return data


def get_pot_odds(hand_value, element, db):
    element = element + '_odds'
    sql = "select " + element + " from pot_odds where hand_value = $1"
    data = db.query.first(sql, str(hand_value))
    return data


def get_valid_stack_value_to_push(hand, db):
    data = db.query(
        "select stack_value from sklansky_chubukov where hand = " + "'" + hand + "'")
    return data[0]['stack_value']


def get_combination_value(element, hand_value, db):
    sql = "select trim(" + element + ") as " + element +" from combination_value where hand_value = $1"
    data = db.query.first(sql, str(hand_value))
    return data