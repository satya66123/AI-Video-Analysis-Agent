import os


class ChatExport:

    @staticmethod
    def export_markdown(history, filename):

        os.makedirs("exports", exist_ok=True)

        path = os.path.join(
            "exports",
            filename + ".md"
        )

        with open(path, "w", encoding="utf-8") as f:

            f.write("# AI Chat\n\n")

            for chat in history:

                f.write(f"## User\n\n")
                f.write(chat["user"] + "\n\n")

                f.write("## Assistant\n\n")
                f.write(chat["assistant"] + "\n\n")

                f.write("---\n\n")

        return path