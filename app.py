import os
import streamlit as st # type: ignore
from PIL import Image
import pdf2image

from dotenv import load_dotenv # type: ignore
load_dotenv()

import google.generativeai as genai # type: ignore
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

import io
import base64

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([
        input, pdf_content[0], prompt
    ])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Let's convert this PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode() #encoding to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

## Creating the Streamlit and prompt template

st.set_page_config(page_title="ATS Resume Demo")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your Resume in PDF format..",
                                 type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")
submit2 = st.button("Which position best suits this Resume?")
submit3 = st.button("Percentage match with Job Description")

input_prompt1 = """
You are an experienced technical Human Resource Manager. 
Your task is to review the provided resume against the job 
description provided by the user.

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
"""

input_prompt2 = """
You are a seasoned career advisor with deep 
expertise in various industries and job roles. 
Given the following resume, your task is to 
analyze the candidate's qualifications, skills, 
and experience. Based on this analysis, provide a detailed 
recommendation of suitable job positions that align with the 
candidate's profile. 

Resume: 
[Insert resume content here]

Your response should include:
1. A summary of the candidate's strengths and key qualifications.
2. A list of job positions that are well-suited for the candidate.
3. An explanation of why these job positions are a good match for 
the candidate's background.
4. Any additional advice or insights that could help the candidate 
in their job search.

Please ensure your recommendations are specific and tailored to 
the candidate's unique profile.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep 
understanding of job role listed in the job description and deep ATS 
functionality, your task is to evaluate the resume against the provided 
job description. Give me the percentage of match if the resume matches
the job description. 
First the output should come as percentage, then keywords missing and 
last final thoughts should come in the order.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, 
                                       pdf_content, 
                                       input_text)
        st.subheader("The Response is..")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, 
                                       pdf_content, 
                                       input_text)
        st.subheader("The Response is..")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, 
                                       pdf_content, 
                                       input_text)
        st.subheader("The Response is..")
        st.write(response)
    else:
        st.write("Please upload the resume")   