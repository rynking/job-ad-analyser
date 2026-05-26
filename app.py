import anthropic
import streamlit as st
from pypdf import PdfReader
import io

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Page config
st.set_page_config(page_title="Job Ad Analyser", page_icon="📄")
st.title("📄 Job Ad Analyser")
st.write("Paste in a job description and your resume to get a tailored analysis.")

# Initialise history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Job description input
job_ad = st.text_area("Job Description", height=300, placeholder="Paste the job ad here...")

# Resume input — paste or upload
st.subheader("Your Resume")
resume_option = st.radio("How would you like to provide your resume?", ["Paste text", "Upload PDF"])

resume = ""
if resume_option == "Paste text":
    resume = st.text_area("Resume", height=300, placeholder="Paste your resume here...")
else:
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    if uploaded_file:
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        resume = "\n".join([page.extract_text() for page in reader.pages])
        st.success("Resume uploaded successfully!")

# Analysis mode
mode = st.radio("Analysis mode", ["Quick Summary", "Detailed Breakdown"])

# Analyse button
if st.button("Analyse"):
    if not job_ad or not resume:
        st.warning("Please provide both a job description and your resume.")
    else:
        with st.spinner("Analysing..."):

            if mode == "Quick Summary":
                prompt = f"""You are a recruitment expert. Analyse this job description against the resume and give a brief, punchy summary covering:
- Overall match score (out of 10)
- Top 3 strengths the candidate brings
- Top 2 gaps to be aware of
- One line verdict: should they apply?

Keep it concise — no more than 200 words total.

Job Description:
{job_ad}

Resume:
{resume}"""
            else:
                prompt = f"""You are a career coach and recruitment expert. A user has provided a job description and their resume.

Your task is to:
1. Extract the key requirements from the job description (skills, experience, qualifications)
2. Assess how well the resume matches those requirements
3. Identify skill gaps or missing experience
4. Suggest specific ways to tailor the resume or application for this role

Job Description:
{job_ad}

Resume:
{resume}

Provide a clear, structured analysis with headings for each section."""

            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            result = message.content[0].text

            # Save to history
            st.session_state.history.append({
                "mode": mode,
                "job_snippet": job_ad[:80] + "...",
                "result": result
            })

# Display latest result
if st.session_state.history:
    latest = st.session_state.history[-1]
    st.divider()
    st.subheader("Latest Analysis")
    st.markdown(latest["result"])

    # Copy button
    st.code(latest["result"], language=None)
    st.caption("☝️ Click the copy icon in the top right of the box above to copy the analysis.")

    # History section. Persists as long as the browser tab is open, allowing users to refer back to previous analyses without needing to re-run them. 
    if len(st.session_state.history) > 1:
        st.divider()
        st.subheader("Previous Analyses")
        for i, entry in enumerate(reversed(st.session_state.history[:-1])):
            with st.expander(f"Analysis {len(st.session_state.history) - 1 - i} — {entry['mode']} — {entry['job_snippet']}"):
                st.markdown(entry["result"])
                st.code(entry["result"], language=None)