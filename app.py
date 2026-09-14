import os
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
    "Enter a topic, choose your skill level, and generate easy-to-understand "
    "AI-powered study notes."
)

# -----------------------------
# Get API key securely
# -----------------------------
def get_api_key():
    """Read the Groq API key from Streamlit secrets or environment variables."""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        secret_key = None

    return secret_key or os.getenv("GROQ_API_KEY")


# -----------------------------
# Generate study notes
# -----------------------------
def generate_study_pack(topic: str, level: str) -> str:
    """Generate a structured study pack using the Groq API."""
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Groq API key is missing. Add GROQ_API_KEY to Streamlit Secrets "
            "or set it as an environment variable."
        )

    client = Groq(api_key=api_key)

    system_prompt = """
You are a friendly and highly effective study assistant.
Create accurate, clear, well-organized study material for students.
Use simple language and explain difficult terms.
Do not invent facts. If a topic is ambiguous, state your assumption.
"""

    user_prompt = f"""
Create a complete study pack for the following topic:

Topic: {topic}
Skill level: {level}

Use this structure:

# Study Pack: {topic}

## 1. Simple Introduction
Explain the topic in easy language.

## 2. Key Concepts
Explain the most important concepts with short examples.

## 3. Important Terms
Provide a bullet list of important terms and their meanings.

## 4. Detailed Explanation
Explain the topic according to the selected skill level.

## 5. Real-World Examples
Give useful and understandable examples.

## 6. Quick Revision
Summarize the most important points.

## 7. Practice Questions
Create 5 questions suitable for the selected skill level.

## 8. Answers
Provide clear answers to the practice questions.

Use Markdown headings, bullets, and numbered lists.
Keep the content educational, organized, and easy to revise.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=4000,
    )

    return response.choices[0].message.content


# -----------------------------
# User inputs
# -----------------------------
topic = st.text_input(
    "Enter your study topic",
    placeholder="e.g., Python functions, Biology, Contract Law",
)

level = st.selectbox(
    "Select your skill level",
    ["Beginner", "Intermediate", "Advanced"],
)

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
    else:
        with st.spinner("Generating your study pack..."):
            try:
                study_pack = generate_study_pack(topic.strip(), level)

                st.success("Your study pack has been generated!")
                st.markdown(study_pack)

                st.download_button(
                    label="⬇️ Download Study Pack",
                    data=study_pack,
                    file_name="study_pack.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            except ValueError as error:
                st.error(str(error))
            except Exception as error:
                st.error(
                    "Something went wrong while generating the study pack. "
                    "Please check your API key, internet connection, and try again."
                )
                with st.expander("Technical details"):
                    st.code(str(error))

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Built with Python, Streamlit, and Groq API.")
