from input_generator.base_generator import BaseGenerator, BaseConfig

TYPE_FUNCTION = {
    'int': lambda val: val,
    'char': lambda val: chr(val)
}

class LineConfig(BaseConfig):
    def __init__(self, variables: dict[str, tuple[int, str]], config: dict[str, str]):
        pass


class LineGenerator(BaseGenerator):
    def generate(self, variables, sequence, config: LineConfig) -> list[list[str]]:
        line_data = []
        for seq in sequence:
            if seq[0] == '$':
                value, types = variables[seq[1:]]
                line_data.append(TYPE_FUNCTION[types](value))
            else:
                line_data.append(seq)
        return [line_data]

line_generator = LineGenerator()
