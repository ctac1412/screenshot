import current_stack


def test_convert_stack():
    assert current_stack.convert_stack(16) == 17
    assert current_stack.convert_stack(0) == 0