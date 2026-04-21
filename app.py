# Import required libraries for the Streamlit app
import streamlit as st  # Web app framework
import google.generativeai as genai  # Google's Generative AI SDK
from pypdf import PdfReader  # Extract text from PDF files
from docx import Document  # Extract text from Word documents

# Function to extract text from uploaded documents
def extract_text(uploaded_file):
    """
    Extracts text from PDF or DOCX files.
    
    Args:
        uploaded_file: File object from Streamlit file uploader
    
    Returns:
        str: All text extracted from the document
    """
    text = ""
    
    # Check if the uploaded file is a PDF
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)  # Create a PDF reader object
        # Iterate through all pages and extract text
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    # Check if the uploaded file is a Word document (.docx)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)  # Create a Document object
        # Iterate through all paragraphs and extract text
        for para in doc.paragraphs:
            text += para.text + "\n"
    
    return text

# Set the page title
st.title("OakTree Report Summarizer")

# Create a password input field for the user's Google API key
api_key = st.text_input("Enter your Google API key", type="password")

# Only proceed if the user has entered an API key
if api_key:
    # Configure the Google Generative AI library with the provided API key
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model (fast and efficient for text summarization)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Create a file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    
    # Only proceed if a file has been uploaded
    if uploaded_file:
        # Extract all text from the uploaded document
        doc_text = extract_text(uploaded_file)
        
        # Create a button for the user to trigger the summarization
        if st.button("Summarize with OakTree"):
            # Display a spinner while waiting for the API response
            with st.spinner("OakTree is thinking..."):
                # Send the document text to Gemini with a prompt to summarize it
                response = model.generate_content(
                    f"Act as a professional technical analyst specializing in report condensation . You are being used in a Python-based automated workflow to process incoming business reports . Your task is to provide a clear, bulleted summary of the provided text . The summary must be under 300 words and cover only the primary findings and recommended actions . Do not include introductory filler or external information . For example: '- Objective: Increase Q3 revenue; - Status: On track' .:\n\n{doc_text}"
                )
                
                # Display the summary results
                st.subheader("Summary")
                st.write(response.text)