class StdAPIError(Exception):
    """Base exception for StdAPI"""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self):
        msg = super().__str__()

        if self.status_code:
            msg += f" | Status: {self.status_code}"

        if self.response:
            msg += f" | Response: {self.response[:150]}"

        return msg
