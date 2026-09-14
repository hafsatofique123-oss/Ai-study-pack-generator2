
import os
import re
import streamlit as st
from groq import Groq

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="centered",
)

# -----------------------------
# App title and description
# -----------------------------
st.title("📚 AI Study Pack Generator")
st.write(
    "Create a personalized study pack by choosing your topic, skill level, "
    "learning duration, goals, and preferred study sections."
)

# -----------------------------
# Get API key securely
# -----------------------------
def get_api_key():
    """Read the Groq API key from Streamlit Secrets or environment variables."""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        secret_key = None

    return secret_key or os.getenv("GROQ_API_KEY")


# -----------------------------
# Generate study pack
# -----------------------------
def generate_study_pack(
    topic: str,
    level: str,
    duration: str,
    goals: str,
    sections: list[str],
    quiz_questions: int,
) -> str:
    """Generate the selected study pack sections using Groq."""

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Groq API key is missing. Add GROQ_API_KEY to Streamlit "
            "Secrets or set it as an environment variable."
        )

    client = Groq(api_key=api_key)

    selected_sections = []

    # Notes
    if "Notes" in sections:
        selected_sections.append(
            """## Notes

Explain the topic in easy language.
Include an introduction, key concepts, important terms,
detailed explanations, examples, and a quick revision summary."""
        )

    # Flashcards
    if "Flashcards" in sections:
        selected_sections.append(
            """## Flashcards

Create useful question-and-answer flashcards
for quick revision of the topic."""
        )

    # Quiz
    if "Quiz" in sections:
        selected_sections.append(
            f"""## Quiz

Create exactly {quiz_questions} quiz questions suitable
for the selected skill level.

Number every question clearly.
Use four options for multiple-choice questions when appropriate.

## Quiz Answers

Provide the correct answer and a short explanation
for every quiz question."""
        )

    # Study plan
    if "Study Plan" in sections:
        selected_sections.append(
            f"""## Study Plan

Create a realistic study plan for the learning duration
of {duration}.

Break the topic into manageable study sessions
and include revision time."""
        )

    # Exam tips
    if "Exam Tips" in sections:
        selected_sections.append(
            """## Exam Tips

Provide practical exam preparation, revision,
time-management, and answer-writing tips
relevant to this topic."""
        )

    sections_text = "\n\n".join(selected_sections)

    user_prompt = f"""
Create a personalized study pack.

Topic: {topic}
Skill level: {level}
Learning duration: {duration}
Learning goals: {goals or "Understand and revise the topic effectively"}

Include only the following requested sections:

{sections_text}

Requirements:
- Use clear Markdown headings, bullets, and numbered lists.
- Use simple language while matching the selected skill level.
- Keep the material accurate, educational, and well organized.
- Do not add sections that were not requested.
- Do not mention these instructions in the response.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly, accurate, and highly effective "
                    "study assistant. Explain difficult concepts clearly "
                    "and do not invent facts."
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=8000,
    )

    return response.choices[0].message.content


# -----------------------------
# User inputs
# -----------------------------
topic = st.text_input(
    "1. Enter your study topic",
    placeholder="e.g., Python functions, Biology, Contract Law",
)

level = st.selectbox(
    "2. Select your skill level",
    ["Beginner", "Intermediate", "Advanced"],
)

duration = st.selectbox(
    "3. Select your learning duration",
    ["1 day", "3 days", "1 week", "2 weeks", "1 month", "3 months"],
)

goals = st.text_area(
    "4. What are your learning goals?",
    placeholder=(
        "e.g., Prepare for an exam, understand the basics, "
        "learn practical skills, or complete a project."
    ),
    height=100,
)

sections = st.multiselect(
    "5. Choose study pack sections",
    ["Notes", "Flashcards", "Quiz", "Study Plan", "Exam Tips"],
    default=["Notes", "Flashcards", "Quiz"],
)

# -----------------------------
# Custom quiz questions
# -----------------------------
quiz_questions = 10

if "Quiz" in sections:
    quiz_questions = st.number_input(
        "How many quiz questions do you want?",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
        help=(
            "Enter your preferred number of questions. "
            "Very large quizzes may take longer or exceed "
            "the AI model's response limits."
        ),
    )

st.info(
    "You can enter your own quiz question count. "
    "There is no fixed preset such as only 5 or 10 questions."
)

# -----------------------------
# Generate button
# -----------------------------
generate_button = st.button(
    "✨ Generate Study Pack",
    type="primary",
    use_container_width=True,
)

# -----------------------------
# Generate and display result
# -----------------------------
if generate_button:
    if not topic.strip():
        st.warning("Please enter a study topic first.")

    elif not sections:
        st.warning("Please select at least one study pack section.")

    elif "Quiz" in sections and quiz_questions < 1:
        st.warning("Please enter at least one quiz question.")

    else:
        with st.spinner("Generating your personalized study pack..."):
            try:
                study_pack = generate_study_pack(
                    topic=topic.strip(),
                    level=level,
                    duration=duration,
                    goals=goals.strip(),
                    sections=sections,
                    quiz_questions=int(quiz_questions),
                )

                st.success("Your study pack has been generated!")

                st.markdown(study_pack)

                safe_topic = re.sub(
                    r"[^a-zA-Z0-9_-]+",
                    "_",
                    topic.strip(),
                )[:50]

                file_name = (
                    f"{safe_topic or 'study_pack'}_study_pack.md"
                )

                st.download_button(
                    label="⬇️ Download Study Pack",
                    data=study_pack,
                    file_name=file_name,
                    mime="text/markdown",
                    use_container_width=True,
                )

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(
                    "Something went wrong while generating the study pack. "
                    "Please check your API key, internet connection, "
                    "and try again."
                )

                with st.expander("Technical details"):
                    st.code(str(error))


# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Built with Python, Streamlit, and Groq API.")
