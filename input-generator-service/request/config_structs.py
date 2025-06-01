from dataclasses import dataclass, field


@dataclass
class Output:
    sequence: list[str]
    separator: str = ' '
    end_line: str = '\n'

@dataclass
class Variable:
    name: str
    range: list[list[int]]
    type: str = 'int'

@dataclass
class TestcaseBlockConfig:
    output: Output
    repeat: str = '1'
    type: str = 'line'
    variable: list[Variable] = field(default_factory=list)
    config: dict[str, object] = field(default_factory=dict)

@dataclass
class TestcaseConfig:
    variable_format: list[Variable]
    lines: list[TestcaseBlockConfig]
