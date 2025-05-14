from abc import ABC, abstractmethod

class BaseConfig(ABC):
    @abstractmethod
    def __init__(self, variables: dict[str, tuple[int, str]], config: dict[str, str]):
        raise NotImplementedError

class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, variables: dict[str, tuple[int, str]], sequence: list[str], config: BaseConfig) -> list[list[str]]:
        raise NotImplementedError
