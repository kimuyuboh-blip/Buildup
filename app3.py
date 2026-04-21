import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
from docx import Document
import io

# --- Functions ---
def extract_text(uploaded_file):
    """Extracts text from PDF or DOCX files."""
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return text

# --- App Setup ---
st.set_page_config(page_title="OakTree Summarizer", page_icon="🌳")
st.title("🌳 OakTree Report Summarizer")

# --- Security: API Key Management ---
# Best Practice: Use st.secrets or environment variables, not hardcoding
api_key = st.secrets.get("OPENAI_API_KEY") 
if not api_key:
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar or setup secrets.toml")
        st.stop()

# --- Initialize Client ---
client = OpenAI(api_key=api_key)

# --- Session State Management ---
if "summary" not in st.session_state:
    st.session_state.summary = ""

# --- UI Components ---
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file:
    # Use st.cache_data to avoid re-extracting text on every rerun
    with st.spinner("Extracting text..."):
        doc_text = extract_text(uploaded_file)
    
    if st.button("Summarize with OakTree"):
        with st.spinner("OakTree is analyzing..."):
            try:
                # OpenAI Chat Completion call
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "Context: You are a professional technical analyst for OakTree specializing in report condensation. "
                                "Task: Provide a clear, bulleted summary of the provided text. "
                                "Constraints: Maximum 300 words. Cover ONLY primary findings and recommended actions. "
                                "No introductory filler or external info. Format: Use clean bullet points."
                            )
                        },
                        {
                            "role": "user", 
                            "content": f"Please summarize the following report content:\n\n{doc_text}"
                        }
                    ],
                    max_tokens=500,
                    temperature=0.3 # Lower temperature for more focused, professional output
                )
                
                # Store the result
                st.session_state.summary = response.choices[0].message.content
            except Exception as e:
                st.error(f"❌ OpenAI Error: {str(e)}")

# --- Display Results ---
if st.session_state.summary:
    st.subheader("Summary")
    st.write(st.session_state.summary)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download Summary",
            data=st.session_state.summary,
            file_name="OakTree_Summary.txt",
            mime="text/plain"
        )
    with col2:
        if st.button("Clear Results"):
            st.session_state.summary = ""
            st.rerun()
