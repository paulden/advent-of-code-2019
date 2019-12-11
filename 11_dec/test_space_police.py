from space_police import paint_panels


def test_paint_panels_should_paint_first_panel_in_0_0():
    initial_position = (0, 0)
    initial_direction = 'U'
    move_instruction = (1, 0)
    painted_panels = {}
    painted_panels_after_move, next_position, next_direction = paint_panels(painted_panels,
                                                                            move_instruction,
                                                                            initial_position,
                                                                            initial_direction)

    assert painted_panels_after_move == {(0, 0): 1}


def test_paint_panels_should_move_robot_to_left_panel_after_receiving_instruction_to_go_left():
    initial_position = (0, 0)
    initial_direction = 'U'
    move_instruction = (1, 0)
    painted_panels = {}
    painted_panels_after_move, next_position, next_direction = paint_panels(painted_panels,
                                                                            move_instruction,
                                                                            initial_position,
                                                                            initial_direction)

    assert next_position == (-1, 0)
    assert next_direction == 'L'


def test_paint_panels_should_move_robot_to_right_panel_after_receiving_instruction_to_go_right():
    initial_position = (0, 0)
    initial_direction = 'U'
    move_instruction = (1, 1)
    painted_panels = {}
    painted_panels_after_move, next_position, next_direction = paint_panels(painted_panels,
                                                                            move_instruction,
                                                                            initial_position,
                                                                            initial_direction)

    assert next_position == (1, 0)
    assert next_direction == 'R'
