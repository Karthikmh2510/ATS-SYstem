import os
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini 1.5 Flash model response 15 Req/min and 1500 Req/day
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

# Gemini 1.5 Pro model response 2 Req/min and 50 req/day
def get_gemini_pro_response(input):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(input)
    return response.text

# Get pdf text
def input_pdf_file(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text

# Creating the prompt template
input_prompt1 = """
Act like, you are a experienced technical Human Resource Manager 
along with skilled ATS (Application Tracking System) with a deep 
understanding of the job title given in the job description.
Your task is to evaluate the provided resume against the job 
description provided by the user.
You must consider the job market is very competitive and you should
provide best assistance for improving the resumes.
Assign the percentage match based on the job description and the 
missing keywords with high accuracy.

resume:{text}
description: {job_description}

Please provide a comprehensive evaluation of the candidate's 
suitability for the role based on the following criteria:
1. Relevance of work experience
2. Skills and qualifications
3. Education background
4. Achievements and certifications
5. Overall alignment with the job requirements

Highlight the candidate's strengths and weaknesses in relation to 
the specified job requirements. Conclude with a summary assessment 
and a recommendation on whether the candidate should be considered 
for the role.

Specify which keywords are missing in the resume and Percentage 
Match of the resume and job description.
"""

input_prompt2 = """
Act as an experienced career coach and resume expert. 
Your task is to provide detailed guidance on how to draft an 
effective resume for an entry-level position. Consider the 
competitive job market and aim to provide the best assistance for 
improving resumes. The guidance should cover the following areas:

1. **What to Include:**
    - Contact Information
    - Objective or Summary
    - Education Background
    - Relevant Skills
    - Work Experience (including internships and volunteer work)
    - Certifications and Achievements
    - Relevant Projects
    - Professional Affiliations (if any)
    - Hobbies and Interests (optional, if they add value)

2. **What to Exclude:**
    - Irrelevant Work Experience
    - Personal Information (such as age, marital status, or photo)
    - Unprofessional Email Addresses
    - Excessive Details on Minor Job Roles
    - Any Negative Language or Information

3. **Tone and Sentence Structure:**
    - Use a professional and positive tone.
    - Be concise and to the point.
    - Use strong action verbs to describe duties and achievements.
    - Avoid the repetations of the words, you must repeat a single strong
      action verbs at most 2 times, but not more than 2 times.
    - Quantify achievements where possible (e.g., "Increased sales 
      by 20%").

4. **Suggestions for Changes:**
    - Provide specific examples of old and corrected sentences.
    - Highlight common mistakes and improvements.

For the given resume content, offer a comprehensive evaluation and 
suggest necessary modifications to align with the above guidelines. 
Provide clear, constructive feedback on each section of the resume.

**Resume Content:**
{resume_content}

**Evaluation and Suggestions:**

1. **Contact Information:**
    - [Evaluate the current contact information and suggest 
      improvements if needed]

2. **Objective or Summary:**
    - Old Sentence: {old_objective_sentence}
    - Corrected Sentence: {corrected_objective_sentence}

3. **Education Background:**
    - [Evaluate the education section and suggest additions or 
    refinements]

4. **Relevant Skills:**
    - Old Sentence: {old_skill_sentence}
    - Corrected Sentence: {corrected_skill_sentence}

5. **Work Experience:**
    - Old Sentence: {old_work_experience_sentence}
    - Corrected Sentence: {corrected_work_experience_sentence}

6. **Certifications and Achievements:**
    - [Evaluate and suggest improvements if needed]

7. **Relevant Projects:**
    - Old Sentence: {old_project_sentence}
    - Corrected Sentence: {corrected_project_sentence}

8. **Professional Affiliations:**
    - [Evaluate and suggest improvements if needed]

9. **Hobbies and Interests:**
    - [Evaluate and suggest if they should be included or excluded]

**Overall Feedback and Recommendations:**
- Provide a summary of the strengths and weaknesses.
- Highlight key areas for improvement.
- Offer a final recommendation on the overall presentation and 
  content of the resume.

Ensure the feedback is detailed, specific, and actionable to help 
the user create a strong, competitive resume for entry-level 
positions.
"""

## Creating the Streamlit 
st.set_page_config(page_title="Smart ATS Resume Demo")
st.header("Improve your Resume with ATS")
job_description = st.text_area("Paste your Job Description: ")
uploaded_file = st.file_uploader("Upload your Resume",
                                 type=["pdf"],
                                 help="Please upload the PDF")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Feedback with respect to the Job Description")
submit2 = st.button("Suggesting some changes in the Resume")
submit3 = st.button("Resume correction in detail (Limit: 2 Requests/min)")

# Function to correct sentences (example implementation)
def correct_sentences(resume_text):
    old_sentences = {
        "old_objective_sentence": "Seeking an entry-level position to start my career.",
        "old_skill_sentence": "Good at Python and Machine Learning.",
        "old_work_experience_sentence": "Worked as an intern at XYZ Corp.",
        "old_project_sentence": "Created a machine learning model for predicting sales."
    }
    corrected_sentences = {
        "corrected_objective_sentence": "Aspiring to secure an entry-level position where I can apply my skills in Python and Machine Learning to contribute to the company's success.",
        "corrected_skill_sentence": "Proficient in Python and experienced with Machine Learning techniques.",
        "corrected_work_experience_sentence": "Completed an internship at XYZ Corp, where I developed practical skills in data analysis and machine learning.",
        "corrected_project_sentence": "Developed a machine learning model to accurately predict sales, improving forecasting accuracy by 15%."
    }
    return old_sentences, corrected_sentences


if submit1:
    if uploaded_file is not None:
        text = input_pdf_file(uploaded_file)
        formatted_input = input_prompt1.format(text=text, job_description=job_description)
        response = get_gemini_response(formatted_input)
        st.subheader("The Response is..")
        st.write(response)
    else:
        st.error("Please upload a PDF file.")
elif submit2:
    if uploaded_file is not None:
        text = input_pdf_file(uploaded_file)
        old_sentences, corrected_sentences = correct_sentences(text)

        formatted_input = input_prompt2.format(
            resume_content=text,
            old_objective_sentence=old_sentences["old_objective_sentence"],
            corrected_objective_sentence=corrected_sentences["corrected_objective_sentence"],
            old_skill_sentence=old_sentences["old_skill_sentence"],
            corrected_skill_sentence=corrected_sentences["corrected_skill_sentence"],
            old_work_experience_sentence=old_sentences["old_work_experience_sentence"],
            corrected_work_experience_sentence=corrected_sentences["corrected_work_experience_sentence"],
            old_project_sentence=old_sentences["old_project_sentence"],
            corrected_project_sentence=corrected_sentences["corrected_project_sentence"]
        )
        
        response = get_gemini_response(formatted_input)
        st.subheader(response)
    else:
        st.error("Please upload a PDF file.")
elif submit3:
    if uploaded_file is not None:
        text = input_pdf_file(uploaded_file)
        old_sentences, corrected_sentences = correct_sentences(text)

        formatted_input = input_prompt2.format(
            resume_content=text,
            old_objective_sentence=old_sentences["old_objective_sentence"],
            corrected_objective_sentence=corrected_sentences["corrected_objective_sentence"],
            old_skill_sentence=old_sentences["old_skill_sentence"],
            corrected_skill_sentence=corrected_sentences["corrected_skill_sentence"],
            old_work_experience_sentence=old_sentences["old_work_experience_sentence"],
            corrected_work_experience_sentence=corrected_sentences["corrected_work_experience_sentence"],
            old_project_sentence=old_sentences["old_project_sentence"],
            corrected_project_sentence=corrected_sentences["corrected_project_sentence"]
        )
        
        response = get_gemini_pro_response(formatted_input)
        st.subheader(response)
    else:
        st.error("Please upload a PDF file.")




