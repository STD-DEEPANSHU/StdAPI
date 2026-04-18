class StdAPIError(Exception):
    """Base exception for StdAPI"""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: str | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        msg = super().__str__()

        if self.status_code is not None:
            msg += f" | Status: {self.status_code}"

        if self.response:
            preview = self.response.strip().replace("\n", " ")[:150]
            msg += f" | Response: {preview}"

        return msg
