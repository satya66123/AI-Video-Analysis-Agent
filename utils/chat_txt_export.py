
import os


class ChatTXTExport:

    @staticmethod
    def export(history, filename):

        os.makedirs("exports", exist_ok=True)

        path = os.path.join(
            "exports",
            filename + ".txt",
        )

        with open(path, "w", encoding="utf-8") as file:

            for chat in history:

                file.write("User\n")
                file.write(chat["user"])
                file.write("\n\n")

                file.write("Assistant\n")
                file.write(chat["assistant"])
                file.write("\n\n")

                file.write("----------------------------------\n")

        return path