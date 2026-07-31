import json
import os


class ChatHistory:

    def __init__(self):
        self.folder = "chat_history"
        os.makedirs(self.folder, exist_ok=True)

    def list_sessions(self):

        return sorted(
            os.listdir(self.folder),
            reverse=True,
        )

    def load(self, filename):

        path = os.path.join(self.folder, filename)

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def save(self, filename, history):

        path = os.path.join(self.folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def delete(self, filename):

        path = os.path.join(self.folder, filename)

        if os.path.exists(path):
            os.remove(path)