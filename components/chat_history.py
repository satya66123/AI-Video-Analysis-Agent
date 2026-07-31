import json
import os

import streamlit as st


class ChatHistory:

    def __init__(self):
        self.chat_dir = "chat_history"
        os.makedirs(self.chat_dir, exist_ok=True)

    def rename(self, old_name, new_name):

        old_path = os.path.join(self.chat_dir, old_name)

        if not new_name.endswith(".json"):
            new_name += ".json"

        new_path = os.path.join(self.chat_dir, new_name)

        if os.path.exists(new_path):
            return False

        os.rename(old_path, new_path)

        return True

    def get_chat_files(self):

        files = [
            f
            for f in os.listdir(self.chat_dir)
            if f.endswith(".json")
        ]

        return sorted(files, reverse=True)

    def render(self):

        st.subheader("📂 Chat History")

        files = self.get_chat_files()

        if not files:
            st.info("No saved chats found.")
            return

        search = st.text_input(
            "🔍 Search Chats",
            placeholder="Search chats..."
        )

        if search:
            files = [
                f
                for f in files
                if search.lower() in f.lower()
            ]

        for file in files:

            with st.expander(f"💬 {file.replace('.json', '')}"):

                path = os.path.join(
                    self.chat_dir,
                    file,
                )

                with open(
                        path,
                        "r",
                        encoding="utf-8",
                ) as f:

                    history = json.load(f)

                st.write(f"**Messages:** {len(history)}")

                if history:
                    st.caption(history[0]["user"][:120])

                st.divider()

                col1, col2, col3 = st.columns(3)

                # ------------------------
                # LOAD
                # ------------------------

                with col1:

                    if st.button(
                            "📂 Load",
                            key=f"load_{file}",
                            use_container_width=True,
                    ):
                        st.session_state.chat_history = history
                        st.success("Chat loaded.")
                        st.rerun()

                # ------------------------
                # DELETE
                # ------------------------

                with col3:

                    if st.button(
                            "🗑 Delete",
                            key=f"delete_{file}",
                            use_container_width=True,
                    ):
                        os.remove(path)

                        st.success("Chat deleted.")

                        st.rerun()

                # ------------------------
                # RENAME
                # ------------------------

                with col2:

                    # ------------------------
                    # RENAME
                    # ------------------------

                    with st.expander("✏ Rename Chat"):

                        new_name = st.text_input(
                            "New Chat Name",
                            value=file.replace(".json", ""),
                            key=f"rename_{file}",
                        )

                        if st.button(
                                "💾 Save Name",
                                key=f"rename_btn_{file}",
                                use_container_width=True,
                        ):

                            if not new_name.strip():

                                st.warning("Please enter a chat name.")

                            else:

                                success = self.rename(
                                    file,
                                    new_name.strip(),
                                )

                                if success:

                                    st.success("✅ Chat renamed successfully.")

                                    st.rerun()

                                else:

                                    st.error("❌ Chat name already exists.")