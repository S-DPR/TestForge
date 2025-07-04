class ConfigValueError(ValueError):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        message = f"Config key '{key}'에서 에러가 발생했습니다. {reason}"
        super().__init__(message)

class VariableNotFoundError(ValueError):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        message = f"{key} 변수를 찾을 수 없습니다. {reason}"
        super().__init__(message)

class PresetNotFoundError(ValueError):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        message = f"{key}라는 ID를 가진 프리셋이 존재하지 않습니다. {reason}"
        super().__init__(message)
