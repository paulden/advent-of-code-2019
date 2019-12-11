BUFFER_FIRST_INSTRUCTION = '00000'

ADDITION_OPCODE = 1
MULTIPLICATION_OPCODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
JUMP_IF_TRUE_OPCODE = 5
JUMP_IF_FALSE_OPCODE = 6
LESS_THAN_OPCODE = 7
EQUALS_OPCODE = 8
ADJUST_RELATIVE_BASE_OPCODE = 9
EXIT_SEQUENCE_CODE = 99


class PaintingRobot:

    def __init__(self, input_program, pointer=0, relative_base=0):
        self.memory_state = input_program.copy()
        self.pointer = pointer
        self.relative_base = relative_base
        # self.latest_output = 0

    def run(self, input_value):
        first_input, second_input = input_value, None

        output = 0
        should_use_first_input_instruction = True

        while self.memory_state[self.pointer] != EXIT_SEQUENCE_CODE:
            instruction_as_string = BUFFER_FIRST_INSTRUCTION + str(self.memory_state[self.pointer])
            opcode = int(instruction_as_string[-2:])

            first_parameter = self.memory_state[self.pointer + 1]
            first_parameter_mode = int(instruction_as_string[-3])
            first_parameter_is_position_mode = first_parameter_mode == 0
            first_parameter_is_immediate_mode = first_parameter_mode == 1
            first_parameter_is_relative_mode = first_parameter_mode == 2

            second_parameter = self.memory_state[self.pointer + 2]
            second_parameter_mode = int(instruction_as_string[-4])
            second_parameter_is_position_mode = second_parameter_mode == 0
            second_parameter_is_immediate_mode = second_parameter_mode == 1
            second_parameter_is_relative_mode = second_parameter_mode == 2

            if opcode == INPUT_OPCODE:
                if first_parameter_is_position_mode:
                    self.memory_state[first_parameter] = input_value
                else:
                    self.memory_state[self.relative_base + first_parameter] = input_value
                self.pointer += 2
                continue

            if first_parameter_is_position_mode:
                first_parameter_value = self.memory_state[first_parameter]
            elif first_parameter_is_immediate_mode:
                first_parameter_value = first_parameter
            elif first_parameter_is_relative_mode:
                first_parameter_value = self.memory_state[self.relative_base + first_parameter]

            if opcode == OUTPUT_OPCODE:
                output = first_parameter_value
                self.pointer += 2
                break

            if opcode == ADJUST_RELATIVE_BASE_OPCODE:
                self.relative_base += first_parameter_value
                self.pointer += 2
                continue

            if second_parameter_is_position_mode:
                second_parameter_value = self.memory_state[second_parameter]
            elif second_parameter_is_immediate_mode:
                second_parameter_value = second_parameter
            elif second_parameter_is_relative_mode:
                second_parameter_value = self.memory_state[self.relative_base + second_parameter]

            third_parameter = self.memory_state[self.pointer + 3]
            third_parameter_mode = int(instruction_as_string[-5])
            third_parameter_is_position_mode = third_parameter_mode == 0
            third_parameter_position = third_parameter if third_parameter_is_position_mode else self.relative_base + third_parameter

            if opcode == ADDITION_OPCODE:
                self.memory_state[third_parameter_position] = first_parameter_value + second_parameter_value
                self.pointer += 4

            elif opcode == MULTIPLICATION_OPCODE:
                self.memory_state[third_parameter_position] = first_parameter_value * second_parameter_value
                self.pointer += 4

            elif opcode == JUMP_IF_TRUE_OPCODE:
                self.pointer = second_parameter_value if first_parameter_value != 0 else self.pointer + 3
            elif opcode == JUMP_IF_FALSE_OPCODE:
                self.pointer = second_parameter_value if first_parameter_value == 0 else self.pointer + 3
            elif opcode == LESS_THAN_OPCODE:
                self.memory_state[third_parameter_position] = 1 if first_parameter_value < second_parameter_value else 0
                self.pointer += 4
            elif opcode == EQUALS_OPCODE:
                self.memory_state[third_parameter_position] = 1 if first_parameter_value == second_parameter_value else 0
                self.pointer += 4

        # self.latest_output = output if output > 0 else self.latest_output
        return output

    def is_halted(self):
        return self.memory_state[self.pointer] == EXIT_SEQUENCE_CODE
