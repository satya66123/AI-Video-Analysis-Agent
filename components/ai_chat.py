import os
from datetime import datetime

import streamlit as st

from components.chat_history import ChatHistory
from services.ai_chat_service import AIChatService
from utils.chat_export import ChatExport

from utils.chat_title import ChatTitle

title_generator = ChatTitle()

from utils.chat_txt_export import ChatTXTExport

txt_export = ChatTXTExport()

from utils.chat_pdf_export import ChatPDFExport

pdf_export = ChatPDFExport()

TRANSCRIPT_DIR = "transcripts"

chat_service = AIChatService()
chat_history_component = ChatHistory()
chat_export = ChatExport()


def get_transcripts():
    if not os.path.exists(TRANSCRIPT_DIR):
        return []

    return sorted(
        [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".txt")],
        reverse=True,
    )


def show_ai_chat_component():
    st.title("💬 AI Chat")

    transcripts = get_transcripts()

    if not transcripts:
        st.warning("No transcripts found. Please generate a transcript first.")
        return

    selected_file = st.selectbox("Select Transcript", transcripts)

    transcript_path = os.path.join(TRANSCRIPT_DIR, selected_file)

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    provider = st.session_state.get("provider")
    model = st.session_state.get("model")

    if not provider or not model:
        st.error("Please select an AI provider and model.")
        return

    st.caption(f"📄 Transcript: {selected_file}")

    c1, c2 = st.columns(2)
    c1.info(f"🤖 Provider: {provider}")
    c2.info(f"🧠 Model: {model}")

    c1, c2 = st.columns(2)

    if c1.button("🆕 New Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if c2.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["user"])

        with st.chat_message("assistant"):
            st.markdown(chat["assistant"])
            st.code(chat["assistant"], language="markdown")

    question = st.chat_input("Ask a question about this transcript...")

    if question:
        with st.spinner("Thinking..."):
            response = st.write_stream(

                chat_service.ask_stream(

                    transcript=transcript,

                    history=st.session_state.chat_history,

                    question=question,

                    provider_name=provider,

                    model_name=model,

                )

            )

            answer = response

        st.session_state.chat_history.append(
            {"user": question, "assistant": answer}
        )
        st.rerun()

    st.divider()

    if st.session_state.chat_history:
        if st.button("💾 Save Chat", use_container_width=True):
            if st.session_state.chat_history:

                first_question = st.session_state.chat_history[0]["user"]

                title = title_generator.generate(first_question)

            else:

                title = "Chat"

            filename = (
                f"{title}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            chat_service.save_chat(filename, st.session_state.chat_history)
            st.success(f"Chat saved as {filename}")

    st.divider()

    st.subheader("📊 Chat Statistics")

    user_messages = len(st.session_state.chat_history)
    assistant_messages = user_messages
    total_messages = user_messages + assistant_messages

    words = 0
    for chat in st.session_state.chat_history:
        words += len(chat["user"].split())
        words += len(chat["assistant"].split())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("User", user_messages)
    c2.metric("Assistant", assistant_messages)
    c3.metric("Total", total_messages)
    c4.metric("Words", words)

    st.divider()

    st.subheader("📤 Export Chat")

    if st.session_state.chat_history:
        export_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        markdown_path = chat_export.export_markdown(
            st.session_state.chat_history,
            export_name,
        )

        with open(markdown_path, "rb") as f:
            st.download_button(
                "⬇ Download Markdown",
                data=f,
                file_name=f"{export_name}.md",
                mime="text/markdown",
                use_container_width=True,
            )
    else:
        st.info("No conversation available.")

    if st.session_state.chat_history:
        pdf_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        pdf_path = pdf_export.export(
            history=st.session_state.chat_history,
            transcript_name=selected_file,
            provider=provider,
            model=model,
            filename=pdf_name,
        )

        with open(pdf_path, "rb") as file:
            st.download_button(
                "📄 Download PDF",
                data=file,
                file_name=f"{pdf_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        txt_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        txt_path = txt_export.export(
            st.session_state.chat_history,
            txt_name,
        )

        with open(txt_path, "rb") as file:
            st.download_button(
                "📝 Download TXT",
                data=file,
                file_name=f"{txt_name}.txt",
                mime="text/plain",
                use_container_width=True,
            )


    st.divider()

    chat_history_component.render()
