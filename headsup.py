import cv2
import math
import time
import datetime
import image_processing
import current_stack
import db_query


def search_opponent_card(screen_area, db, stack_collection=0, is_postflop=False):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        opponent_area = save_opponent_card_image(screen_area, folder_name, db)[0]
        check_is_headsup = 0
        card_area = db_query.get_opponent_card_area(screen_area, db)
        opponent_data = []
        last_screen = db_query.get_last_screen(card_area, db, 2)
        last_screen = last_screen[::-1]
        for item in last_screen:
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            template_path = 'is_headsup/is_headsup.png'
            if image_processing.cv_data_template(template_path, img_rgb) > 0:
                check_is_headsup += 1
                if is_postflop is False:
                    opponent_data.append(
                        current_stack.search_opponent_stack(screen_area, opponent_area, stack_collection, db))
            opponent_area += 1
        if check_is_headsup != 1:
            check_is_headsup = 0
        opponent_data.insert(0, check_is_headsup)
        return opponent_data
    except Exception as e:
        print(e)


def save_opponent_card_image(screen_area, folder_name, db):
    image_name = int(math.floor(time.time()))
    opponent_area = []
    for val in db_query.get_opponent_card_data(screen_area, db):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                 val['screen_area'], db)
        image_name += 1
        opponent_area.append(val['opponent_area'])
    return opponent_area
