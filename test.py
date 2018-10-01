element_area = saveElement(screen_area, 'action_btn_area')
    if image_processing.searchElement(element_area, ['raise_to', 'call'], 'action_buttons/'):
        condition = session_log.getLastRowFromLogSession(str(screen_area))
        logic.getDecision(condition[0]['hand'], condition[0]['current_stack'], condition[0]['current_position'],
                          str(screen_area), condition[0]['action'])
        return True