class CreateTestcaseError(ValueError):
    def __init__(self, details: str):
        self.details = details
        message = details
        super().__init__(message)