import streamlit as st
from google import genai


st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered"
)


# -------------------------
# Gemini Configuration
# -------------------------

api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)


# -------------------------
# Email Generator
# -------------------------

def generate_email(
    purpose,
    recipient,
    key_points,
    tone,
    context,
    length
):

    prompt = f"""
You are a professional AI email writing assistant.

Generate a high-quality email based on the following information.

Email Purpose:
{purpose}

Recipient:
{recipient}

Key Points:
{key_points}

Tone:
{tone}

Additional Context:
{context}

Desired Length:
{length}

Instructions:
- Create a suitable subject line.
- Write a natural and professional email.
- Do not invent facts.
- Keep the message clear and relevant.
- Match the requested tone.
- Avoid unnecessary repetition.
- Include an appropriate greeting and closing.

Return the response exactly in this format:

Subject:
<subject>

Email:
<email>
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


# -------------------------
# UI
# -------------------------

st.title("✉️ AI Email Generator")

st.write(
    "Create professional emails in seconds using Google Gemini AI."
)


purpose = st.selectbox(
    "Email Purpose",
    [
        "Job Application",
        "Follow-up",
        "Client Proposal",
        "Thank You",
        "Meeting Request",
        "Complaint",
        "General"
    ]
)


recipient = st.text_input(
    "Recipient",
    placeholder="e.g. Client, Hiring Manager, Professor"
)


key_points = st.text_area(
    "What do you want to say?",
    placeholder="Enter the main points you want to include..."
)


tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Formal",
        "Concise"
    ]
)


context = st.text_area(
    "Additional Context (Optional)",
    placeholder="Add any additional information..."
)


length = st.selectbox(
    "Email Length",
    [
        "Short",
        "Medium",
        "Detailed"
    ]
)


if st.button("✨ Generate Email", use_container_width=True):

    if not key_points.strip():
        st.warning("Please enter what you want to say.")

    else:

        with st.spinner("Writing your email..."):

            try:

                result = generate_email(
                    purpose,
                    recipient,
                    key_points,
                    tone,
                    context,
                    length
                )

                st.success("Email generated successfully!")

                st.markdown(result)

                st.text_area(
                    "Copy your email",
                    result,
                    height=350
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )
