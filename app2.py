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

# Initialize session state keys for Streamlit to store the summary result
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Create a password input field for the user's Google API key
api_key = "AIzaSyCyw_ODKNrYMOO4gJbJHI3F-_ZVfzlQF7g"


if api_key:
    genai.configure(api_key=api_key)
    
    # 1. Applying "Context" and "Constraints" via system_instruction
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash', # Updated to a valid model version
        system_instruction=(
            "Context: You are a professional technical analyst for OakTree specializing in report condensation. "
            "Task: Provide a clear, bulleted summary of the provided text. "
            "Constraints: Maximum 300 words. Cover ONLY primary findings and recommended actions. "
            "No introductory filler or external info. Format: Use clean bullet points."
        )
    )
    
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    
    if uploaded_file:
        doc_text = extract_text(uploaded_file)
        
        if st.button("Summarize with OakTree"):
            with st.spinner("OakTree is thinking..."):
                try:
                    # 2. Sending only the "Task" and data in the main prompt
                    response = model.generate_content(
                        f"Please summarize the following report content according to your instructions:\n\n{doc_text}"
                    )
                    # Store the result in session state
                    st.session_state.summary = response.text
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}\n\nMake sure your API key is valid. Get one from: https://aistudio.google.com/")


    # Check if there is a summary in session state to display
    if st.session_state.summary:
        st.subheader("Summary")
        st.write(st.session_state.summary)

        # Create two columns for the action buttons
        col1, col2 = st.columns(2)
               
        # Download button uses the data stored in session state
        with col1:
            st.download_button(
                label="Download Summary",
                data=st.session_state.summary,
                file_name="OakTree_Summary.txt",
                mime="text/plain"
            )

         # Add a clear button to reset the app
        with col2:
            if st.button("Clear Results"):
                st.session_state.summary = ""
                st.rerun()