from request.config_structs import Output, LineConfigDataclass
from input_generator.base_generator import BaseGenerator, BaseConfig, TYPE_FUNCTION


class LineConfig(BaseConfig):
    def __init__(self, variables: dict[str, tuple[int, str]], config: LineConfigDataclass):
        pass


class LineGenerator(BaseGenerator):
    def generate(self, variables, output: Output, config: LineConfig) -> list[list[str]]:
        line_data = []
        for seq in output.sequence:
            if seq[0] == '$':
                value, types = variables[seq[1:]]
                line_data.append(str(TYPE_FUNCTION[types](value)))
            else:
                line_data.append(seq)
        return [line_data]

line_generator = LineGenerator()
