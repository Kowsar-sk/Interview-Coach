import streamlit as st
import fitz  # PyMuPDF
import docx
import tempfile
import os

# Function to extract text from PDF
def extract_text_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    except Exception:
        text = ""
    return text

# Function to extract text from DOCX
def extract_text_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception:
        text = ""
    return text

# Placeholder function to generate interview questions
def generate_questions(resume_text, job_role):
    return [
        f"What motivated you to pursue a career in {job_role}?",
        f"Can you describe a project from your resume that aligns with the {job_role} role?",
        f"What are the key skills you bring to a {job_role} position?",
        f"How do you stay updated with trends in {job_role}?",
        f"Describe a challenge you faced in your previous role and how you overcame it."
    ]

# Placeholder function to provide feedback on answers
def get_feedback(question, answer):
    return (
        f"**Feedback for:** \"{question}\"\n"
        f"- Clarity: Good\n"
        f"- Relevance: Matches the question\n"
        f"- Tone: Professional\n"
        f"- Suggested Improvement: Add specific examples or metrics.\n"
        f"- Score: 8/10"
    )

# Streamlit UI
st.title("GenAI-Powered Interview Coach (Local Version)")

uploaded_resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_role = st.text_input("Enter the Job Role you're targeting")

if uploaded_resume and job_role:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_resume.name)[1]) as tmp:
        tmp.write(uploaded_resume.read())
        resume_path = tmp.name

    if uploaded_resume.name.endswith(".pdf"):
        resume_text = extract_text_pdf(resume_path)
    elif uploaded_resume.name.endswith(".docx"):
        resume_text = extract_text_docx(resume_path)
    else:
        resume_text = ""

    st.subheader("Generated Interview Questions")
    questions = generate_questions(resume_text, job_role)

    for i, question in enumerate(questions):
        st.markdown(f"**Q{i+1}: {question}**")
        response = st.text_area(f"Your Answer to Q{i+1}", key=f"answer_{i}")
        if response:
            feedback = get_feedback(question, response)
            st.markdown("**Feedback:**")
            st.markdown(feedback)
