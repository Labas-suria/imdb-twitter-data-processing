class MockRequestResponse:
    """Class responsible for simulating a response to request.get method"""

    def __init__(self, data, status_code, reason=""):
        self.data = data
        self.status_code = status_code
        self.reason = reason

    def json(self):
        return self.data

    @property
    def content(self):
        return bytes(self.data, 'utf-8')
