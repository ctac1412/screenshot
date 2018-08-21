def getElementArea(screen_area, element):
    test = "select " + element + " from screen_coordinates where screen_area = " + str(screen_area) + " and active = 1"
    return test

print(getElementArea(1,'green_area'))




