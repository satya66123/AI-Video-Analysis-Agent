import re


class ChatTitle:

    @staticmethod
    def generate(question):

        title = question.strip()

        title = re.sub(r"[^\w\s-]", "", title)

        title = "_".join(title.split())

        return title[:40]