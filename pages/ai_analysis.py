import os
import streamlit as st

from services.ai_analysis_service import AIAnalysisService
from components.analysis_history import AnalysisHistory

from prompts.summary_prompt import SUMMARY_PROMPT
from prompts.keypoints_prompt import KEYPOINTS_PROMPT
from prompts.actionitems_prompt import ACTIONITEMS_PROMPT
from prompts.meeting_prompt import MEETING_PROMPT
from prompts.study_notes_prompt import STUDY_NOTES_PROMPT
from prompts.sentiment_prompt import SENTIMENT_PROMPT
from prompts.topics_prompt import TOPICS_PROMPT
from prompts.keywords_prompt import KEYWORDS_PROMPT


TRANSCRIPT_FOLDER = "transcripts"

PROMPTS = {
    "Summary": SUMMARY_PROMPT,
    "Key Points": KEYPOINTS_PROMPT,
    "Action Items": ACTIONITEMS_PROMPT,
    "Meeting Minutes": MEETING_PROMPT,
    "Study Notes": STUDY_NOTES_PROMPT,
    "Sentiment Analysis": SENTIMENT_PROMPT,
    "Topics": TOPICS_PROMPT,
    "Keywords": KEYWORDS_PROMPT
}


def get_transcripts():
    """Return available transcript files."""

    if not os.path.exists(TRANSCRIPT_FOLDER):
        return []

    files = [
        f for f in os.listdir(TRANSCRIPT_FOLDER)
        if f.endswith(".txt")
    ]

    files.sort(reverse=True)

    return files


def show_ai_analysis():
    """Reusable AI Analysis Component."""

    st.title("🧠 AI Video Analysis")

    transcripts = get_transcripts()

    if not transcripts:
        st.warning("No transcripts found.")
        return

    provider = st.session_state.get("provider")
    model = st.session_state.get("model")

    if not provider or not model:
        st.error("Please select a Provider and Model from the sidebar.")
        return

    selected_file = st.selectbox(
        "Select Transcript",
        transcripts
    )

    analysis_type = st.selectbox(
        "Analysis Type",
        list(PROMPTS.keys())
    )

    transcript_path = os.path.join(
        TRANSCRIPT_FOLDER,
        selected_file
    )

    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as file:
        transcript = file.read()

    st.subheader("Transcript")

    st.text_area(
        "Transcript",
        transcript,
        height=300,
        disabled=True
    )

    if st.button(
        "🚀 Analyze",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner("Analyzing transcript..."):

            try:

                result = AIAnalysisService.analyze(
                    provider_name=provider,
                    model_name=model,
                    transcript=transcript,
                    prompt=PROMPTS[analysis_type]
                )

                AIAnalysisService.save_analysis(
                    filename=os.path.splitext(selected_file)[0],
                    analysis_type=analysis_type.replace(" ", "_"),
                    content=result
                )

                st.success("✅ Analysis Completed")

                st.subheader("Analysis Result")

                st.markdown(result)

                st.download_button(
                    label="📥 Download Markdown",
                    data=result,
                    file_name=f"{analysis_type}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Analysis Failed: {e}")

    st.divider()

    AnalysisHistory.render()