from abc import ABC, abstractmethod

from dsl.executor import Output


class BaseConfig(ABC):
    @abstractmethod
    def __init__(self, variables: dict[str, tuple[int, str]], config: dict[str, str]):
        raise NotImplementedError

class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, variables: dict[str, tuple[int, str]], output: Output, config: BaseConfig) -> list[list[str]]:
        raise NotImplementedError
