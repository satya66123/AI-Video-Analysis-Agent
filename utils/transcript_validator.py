import os


class TranscriptValidator:

    @staticmethod
    def validate(path):

        if not os.path.exists(path):
            return False

        if os.path.getsize(path) == 0:
            return False

        return True