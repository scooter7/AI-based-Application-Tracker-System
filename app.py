import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pdf_processor import extract_text_from_pdf

# Load environment variables and configure API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Refined ATS prompt
input_prompt_ats = """
You are an elite ATS (Applicant Tracking System) expert with extensive knowledge in tech fields, including software engineering, data science, data analysis, and big data engineering. Your mission is to meticulously evaluate the given resume against the provided job description.

Consider the following:
1. The job market is highly competitive.
2. Provide actionable insights to significantly improve the resume.
3. Conduct a thorough analysis of skills, experience, and qualifications.

Resume: {extracted_text}
Job Description: {jd}

Provide a detailed response in the following format:
### 1. Job Description Match:
   - Overall match percentage
   - Breakdown of match by key areas (skills, experience, qualifications)

### 2. Missing Keywords:
   - List of important keywords from the job description not found in the resume
   - Suggestions on how to incorporate these keywords naturally

### 3. Profile Summary:
   - A concise, impactful summary of the candidate's profile
   - Highlight strengths and unique selling points
   - Suggestions for improvement

### 4. Improvement Recommendations:
   - Specific, actionable steps to enhance the resume
   - Prioritized list of changes to make the resume more competitive

Remember to be constructive, specific, and provide guidance that will genuinely improve the candidate's chances of success.
"""

def main():
    st.set_page_config(page_title="ResumeATS - Application Tracker System", page_icon="📄", layout="wide")
    
    st.title("📄 ResumeATS - Application Tracker System")
    st.markdown("""
    Boost your resume's ATS score and increase your chances of landing that dream job!
    Upload your resume and paste the job description to get personalized insights and improvement recommendations.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Upload Job Description")
        jd = st.text_area("Paste the Job Description here", height=300)

    with col2:
        st.subheader("📤 Upload Your Resume")
        uploaded_file = st.file_uploader("Choose your resume (PDF format)", type="pdf")

    if st.button("🚀 Analyze Resume", type="primary"):
        if uploaded_file is not None and jd:
            with st.spinner("Analyzing your resume... This may take a moment."):
                extracted_text = extract_text_from_pdf(uploaded_file)
                response = model.generate_content(input_prompt_ats.format(extracted_text=extracted_text, jd=jd))
                
                st.success("Analysis complete!")
                st.subheader("🔍 ATS Analysis Results")
                st.markdown(response.text)
        else:
            st.error("Please upload a PDF resume and provide a job description.")

    st.markdown(
        "<div style='text-align: center; margin-top:10px;'>Made with ❤️ by <a style='color: #ffffff;' href='https://github.com/jessjohn1539' target='_blank'>Jess John</a></div>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()