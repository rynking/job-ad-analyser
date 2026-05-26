# Job Ad Analyser

A web application that uses the Claude AI API to help job seekers evaluate how well their resume matches a job description.

## What it does
- Accepts a job description and resume (pasted text or PDF upload)
- Analyses the match between the two using Claude AI
- Offers two modes: Quick Summary (concise score and verdict) or Detailed Breakdown (full analysis with tailored suggestions)
- Keeps a history of previous analyses within the session

## Built with
- [Anthropic Claude API](https://docs.anthropic.com) — AI analysis
- [Streamlit](https://streamlit.io) — web interface and deployment

## Live app
[Click here to use the app](https://job-ad-analyser-slaa.streamlit.app/)

## How to run locally
1. Clone the repo
2. Create a virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Add your Anthropic API key to `.streamlit/secrets.toml`:
ANTHROPIC_API_KEY = "your-key-here"
4. Run the app:
streamlit run app.py