import pytest
import postgresql
import db_query
import session_log


@pytest.mark.parametrize('screen_area, db',(['1', '2', '3', '4'], [postgresql.open(db_query.connection_string())]))
def test_get_hand_value(screen_area, db):
    print(session_log.get_hand_value(screen_area, db))