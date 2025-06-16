from dataclasses import dataclass, field


@dataclass
class Range:
    min: str
    max: str

@dataclass
class IntRange:
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
class MatrixConfigDataclass:
    col_size: str = None
    row_size: str = '1'
    num_type: str = 'int'
    num_range: list[Range] = field(default_factory=list)
    is_distinct: bool = False
    value_limit: dict[str, int] = field(default_factory=dict)
    empty_value: str | None = None
    random_empty: bool = False
    is_graph: bool = False
    is_symmetric: bool = False


@dataclass
class QueryConfigDataclass:
    outputs: list[Output] = None
    distribution: list[str] = field(default_factory=list)
    min_count: list[str] = field(default_factory=list)
    max_count: list[str] = field(default_factory=list)
    repeat: str = '1'


@dataclass
class GraphConfigDataclass:
    node_count: str = None
    edge_count: str = None
    is_zero_start: bool = False
    weight_range: list[Range] = field(default_factory=list)
    is_perfect: bool = False
    is_connect: bool = False
    is_cycle: bool = False


@dataclass
class LineConfigDataclass:
    pass
