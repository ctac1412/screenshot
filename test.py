import image_processing

reac = image_processing.searchLastOpponentAction('2')
if not isinstance(reac, str):
    print(reac['alias'])
# else:
#     print(reac['alias'])
