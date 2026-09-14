import os
import re
import streamlit as st
from groq import Groq


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="centered"
)


# --------------------------------------------------
# Baby Pink UI Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff5f7, #ffe4ec);
        color: #6d3452;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .main .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(135deg, #d96b8b, #b84f76);
        padding: 35px 25px;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(184, 79, 118, 0.25);
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 10px;
        font-weight: 800;
    }

    .hero p {
        color: #fff5f8;
        font-size: 17px;
        margin-bottom: 0;
    }

    .section-card {
        background: rgba(255, 250, 252, 0.95);
        padding: 22px;
        border-radius: 20px;
        border: 1px solid #f3bfd0;
        box-shadow: 0 5px 18px rgba(184, 79, 118, 0.08);
        margin-bottom: 20px;
    }

    .section-title {
        color: #a63d68;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .stTextInput input,
    .stTextArea textarea {
        background-color: #fffafd !important;
        border: 1px solid #efb5c8 !important;
        border-radius: 12px !important;
        color: #6d3452 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #fffafd !important;
        border: 1px solid #efb5c8 !important;
        border-radius: 12px !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #d96b8b, #b84f76);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 12px;
        font-size: 17px;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(184, 79, 118, 0.25);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #b84f76, #963d60);
        color: white;
        border: none;
    }

    .output-card {
        background: #fffafd;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #efb5c8;
        box-shadow: 0 5px 18px rgba(184, 79, 118, 0.10);
    }

    h1, h2, h3 {
        color: #a63d68;
    }

    .stCaption {
        color: #9c5a75;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Hero Section
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>📚 AI Study Pack Generator</h1>
        <p>Create personalized notes, flashcards, quizzes, study plans, and exam tips with AI.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# API Key Function
# --------------------------------------------------

def get_api_key():
    """
    Read the Groq API key from Streamlit Secrets
    or environment variables.
    """

    try:
        secret_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        secret_key = None

    return secret_key or os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# Generate Study Pack Function
# --------------------------------------------------

def generate_study_pack(
    topic,
    level,
    duration,
    goals,
    sections,
    quiz_questions
):
    """
    Generate the selected study pack sections using Groq API.
    """

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Groq API key is missing. Please add GROQ_API_KEY "
            "to Streamlit Secrets."
        )

    client = Groq(api_key=api_key)

    selected_sections = []

    if "Notes" in sections:
        selected_sections.append(
            """
## Notes

Explain the topic in easy language.

Include:

- Introduction
- Key concepts
- Important terms
- Detailed explanations
- Practical examples
- Quick revision summary
"""
        )

    if "Flashcards" in sections:
        selected_sections.append(
            """
## Flashcards

Create useful question-and-answer flashcards
for quick revision.
"""
        )

    if "Quiz" in sections:
        selected_sections.append(
            f"""
## Quiz

Create exactly {quiz_questions} quiz questions
according to the selected skill level.

Number every question clearly.
Provide four options where appropriate.

## Quiz Answers

Provide the correct answer and a short explanation
for every quiz question.
"""
        )

    if "Study Plan" in sections:
        selected_sections.append(
            f"""
## Study Plan

Create a realistic study plan for the learning duration
of {duration}.

Break the topic into manageable study sessions
and include revision time.
"""
        )

    if "Exam Tips" in sections:
        selected_sections.append(
            """
## Exam Tips

Provide practical exam preparation tips,
revision tips, time-management tips,
and answer-writing tips relevant to this topic.
"""
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

- Use clear Markdown headings.
- Use bullets and numbered lists.
- Use simple language according to the selected skill level.
- Keep the material accurate and educational.
- Keep the study pack well organized.
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
            {
                "role": "user",
                "content": user_prompt
            },
        ],
        temperature=0.4,
        max_tokens=8000,
    )

    return response.choices[0].message.content


# --------------------------------------------------
# User Inputs
# --------------------------------------------------

st.markdown(
    '<div class="section-card">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">📝 Create Your Study Pack</div>',
    unsafe_allow_html=True
)

topic = st.text_input(
    "1. Enter your study topic",
    placeholder="e.g., Python functions, Biology, Contract Law"
)

level = st.selectbox(
    "2. Select your skill level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

duration = st.selectbox(
    "3. Select your learning duration",
    [
        "1 day",
        "3 days",
        "1 week",
        "2 weeks",
        "1 month",
        "3 months"
    ]
)

goals = st.text_area(
    "4. What are your learning goals?",
    placeholder=(
        "e.g., Prepare for an exam, understand the basics, "
        "learn practical skills, or complete a project."
    ),
    height=100
)

sections = st.multiselect(
    "5. Choose study pack sections",
    [
        "Notes",
        "Flashcards",
        "Quiz",
        "Study Plan",
        "Exam Tips"
    ],
    default=[
        "Notes",
        "Flashcards",
        "Quiz"
    ]
)

quiz_questions = 10

if "Quiz" in sections:
    quiz_questions = st.number_input(
        "How many quiz questions do you want?",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
        help=(
            "You can enter your preferred number of questions. "
            "Very large quizzes may take longer or exceed "
            "the AI model response limits."
        )
    )

st.info(
    "You can enter your own quiz question count. "
    "There is no fixed preset such as only 5 or 10 questions."
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# Generate Button
# --------------------------------------------------

generate_button = st.button(
    "✨ Generate Study Pack",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Generate and Display Result
# --------------------------------------------------

if generate_button:

    if not topic.strip():
        st.warning("Please enter a study topic first.")

    elif not sections:
        st.warning("Please select at least one study pack section.")

    elif "Quiz" in sections and quiz_questions < 1:
        st.warning("Please enter at least one quiz question.")

    else:

        with st.spinner(
            "Generating your personalized study pack..."
        ):

            try:

                study_pack = generate_study_pack(
                    topic=topic.strip(),
                    level=level,
                    duration=duration,
                    goals=goals.strip(),
                    sections=sections,
                    quiz_questions=int(quiz_questions)
                )

                st.success(
                    "Your study pack has been generated successfully! 🎉"
                )

                st.markdown(
                    '<div class="output-card">',
                    unsafe_allow_html=True
                )

                st.markdown(study_pack)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

                safe_topic = re.sub(
                    r"[^a-zA-Z0-9_-]+",
                    "_",
                    topic.strip()
                )[:50]

                file_name = (
                    f"{safe_topic or 'study_pack'}_study_pack.md"
                )

                st.download_button(
                    label="⬇️ Download Study Pack",
                    data=study_pack,
                    file_name=file_name,
                    mime="text/markdown",
                    use_container_width=True
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


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Built with Python, Streamlit, and Groq API 💗"
)
