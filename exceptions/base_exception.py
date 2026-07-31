"""
exceptions/base_exception.py
"""

class VideoAnalysisException(Exception):

    def __init__(
        self,
        message: str,
    ):

        self.message = message

        super().__init__(message)