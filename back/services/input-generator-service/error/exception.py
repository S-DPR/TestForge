class ConfigValueError(ValueError):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        message = f"Config key '{key}'에서 에러가 발생했습니다. {reason}"
        super().__init__(message)
