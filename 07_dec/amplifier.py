BUFFER_FIRST_INSTRUCTION = '00000'

ADDITION_OPCODE = 1
MULTIPLICATION_OPCODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
JUMP_IF_TRUE_OPCODE = 5
JUMP_IF_FALSE_OPCODE = 6
LESS_THAN_OPCODE = 7
EQUALS_OPCODE = 8
EXIT_SEQUENCE_CODE = 99


class Amplifier:

    def __init__(self, input_program, setting, pointer=0):
        self.memory_state = input_program.copy()
        self.setting = setting
        self.pointer = pointer
        self.is_starting = True
        self.latest_output = 0

    def run(self, input_value):
        first_input, second_input = self._retrieve_inputs(input_value)

        output = 0
        should_use_first_input_instruction = True

        while self.memory_state[self.pointer] != EXIT_SEQUENCE_CODE:
            first_instruction_as_string = BUFFER_FIRST_INSTRUCTION + str(self.memory_state[self.pointer])
            opcode = int(first_instruction_as_string[-2:])

            first_parameter = self.memory_state[self.pointer + 1]
            second_parameter = self.memory_state[self.pointer + 2]

            first_parameter_is_position_mode = int(first_instruction_as_string[-3]) == 0
            second_parameter_is_position_mode = int(first_instruction_as_string[-4]) == 0

            if opcode == INPUT_OPCODE:
                self.memory_state[first_parameter] = first_input if should_use_first_input_instruction else second_input
                should_use_first_input_instruction = False
                self.pointer += 2
                continue

            first_parameter_value = self.memory_state[first_parameter] if first_parameter_is_position_mode else first_parameter

            if opcode == OUTPUT_OPCODE:
                output = first_parameter_value
                self.pointer += 2
                break

            second_parameter_value = self.memory_state[second_parameter] if second_parameter_is_position_mode else second_parameter

            output_position = self.memory_state[self.pointer + 3]
            if opcode == ADDITION_OPCODE:
                self.memory_state[output_position] = first_parameter_value + second_parameter_value
                self.pointer += 4

            elif opcode == MULTIPLICATION_OPCODE:
                self.memory_state[output_position] = first_parameter_value * second_parameter_value
                self.pointer += 4

            elif opcode == JUMP_IF_TRUE_OPCODE:
                self.pointer = second_parameter_value if first_parameter_value != 0 else self.pointer + 3
            elif opcode == JUMP_IF_FALSE_OPCODE:
                self.pointer = second_parameter_value if first_parameter_value == 0 else self.pointer + 3
            elif opcode == LESS_THAN_OPCODE:
                self.memory_state[output_position] = 1 if first_parameter_value < second_parameter_value else 0
                self.pointer += 4
            elif opcode == EQUALS_OPCODE:
                self.memory_state[output_position] = 1 if first_parameter_value == second_parameter_value else 0
                self.pointer += 4

        self.latest_output = output if output > 0 else self.latest_output
        return output

    def _retrieve_inputs(self, input_value):
        if self.is_starting:
            first_input_value = self.setting
            second_input_value = input_value
        else:
            first_input_value = input_value
            second_input_value = None
        self.is_starting = False
        return first_input_value, second_input_value

    def is_halted(self):
        return self.memory_state[self.pointer] == EXIT_SEQUENCE_CODE
