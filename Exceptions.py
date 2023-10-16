class ResultIsEmptyException(Exception):
    def __init__(self, message="ResultIsEmptyException"):
        self.message = message
        super().__init__(self.message)
