from dataclasses import dataclass, field


@dataclass
class Range:
    min: int
    max: int

@dataclass
class Output:
    sequence: list[str]
    separator: str = ' '
    end_line: str = '\n'

@dataclass
class Variable:
    name: str
    range: list[Range]
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


@dataclass
class MatrixConfigDatalist:
    col_size: str = None
    row_size: str = '1'
    num_type: str = 'int'
    num_range: list[Range] = field(default_factory=list)
    is_distinct: bool = False
    value_limit: dict[str, int] = field(default_factory=dict)
    empty_value: str = None
    random_empty: bool = False
    is_graph: bool = False
    is_symmetric: bool = False
