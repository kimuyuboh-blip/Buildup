# ============================================================================
# IMPORTS: Required libraries for the Streamlit web app and AI integration
# ============================================================================
import streamlit as st                  # Web app framework for building UI
from openai import OpenAI              # OpenAI API client for GPT models
from pypdf import PdfReader            # Library to extract text from PDF files
from docx import Document              # Library to extract text from Word documents

# ============================================================================
# FUNCTION 1: chunk_text()
# Purpose: Break large documents into smaller chunks to avoid token limits
# This prevents context window overflow when sending to OpenAI API
# ============================================================================
def chunk_text(text, max_tokens=12000):
    """Simple character-based chunking to stay within context limits."""
    return [text[i : i + max_tokens] for i in range(0, len(text), max_tokens)]

# ============================================================================
# FUNCTION 2: extract_text()
# Purpose: Read and extract text content from uploaded PDF or DOCX files
# Supports both PDF and Word document formats
# ============================================================================
def extract_text(uploaded_file):
    """Extract text from PDF or DOCX files."""
    text = ""
    # Handle PDF files
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        # Loop through each page and extract text
        for page in reader.pages:
            text += page.extract_text() + "\n"
    # Handle Word documents (.docx)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        # Loop through each paragraph and extract text
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text


# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# Sets the browser tab title and page icon
# ============================================================================
st.set_page_config(page_title="OakTree Summarizer", page_icon="🌳")
st.title("OakTree Report Summarizer")

# ============================================================================
# SIDEBAR CONFIGURATION
# Purpose: Collect API key and display user information in a collapsible menu
# The sidebar keeps the main area clean and organized
# ============================================================================
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.info("Your key is not stored. It is used only for the duration of this session.")

# ============================================================================
# SESSION STATE INITIALIZATION
# Purpose: Store the summary result across page reruns in Streamlit
# Session state persists data while the user interacts with the app
# ============================================================================
if "summary" not in st.session_state:
    st.session_state.summary = ""

# ============================================================================
# API KEY VALIDATION
# Purpose: Ensure user has provided an API key before proceeding
# If no key is provided, stop execution and prompt the user
# ============================================================================
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to proceed.")
    st.stop()

# ============================================================================
# INITIALIZE OPENAI CLIENT
# Purpose: Create OpenAI API client with the user's API key for API calls
# ============================================================================
client = OpenAI(api_key=api_key)

# ============================================================================
# FILE UPLOADER WIDGET
# Purpose: Allow users to upload PDF or DOCX files for summarization
# Only accepts these file types to prevent processing unsupported formats
# ============================================================================
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

# ============================================================================
# FILE PROCESSING BLOCK
# Purpose: Handle user interactions after file upload
# ============================================================================
if uploaded_file:
    # Extract text from the uploaded document
    doc_text = extract_text(uploaded_file)
    
    # ========================================================================
    # SUMMARIZATION BUTTON
    # Purpose: Trigger the summarization process when clicked
    # ========================================================================
    if st.button("Summarize with OakTree"):
        # Display a loading indicator while processing
        with st.spinner("OakTree is processing your report..."):
            try:
                # ====================================================================
                # STEP 1: TEXT CHUNKING
                # Purpose: Split large documents into manageable chunks
                # This prevents exceeding OpenAI's token limits per request
                # ====================================================================
                text_chunks = chunk_text(doc_text)
                summaries = []

                # ====================================================================
                # STEP 2: PROCESS EACH CHUNK
                # Purpose: Send each chunk to OpenAI for individual summarization
                # Collects summaries from all chunks
                # ====================================================================
                for i, chunk in enumerate(text_chunks):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a professional technical analyst for OakTree. Summarize findings and recommended actions clearly."},
                            {"role": "user", "content": f"Summarize this part of the report:\n\n{chunk}"}
                        ],
                        max_tokens=400,
                        temperature=0.3
                    )
                    summaries.append(response.choices[0].message.content)

                # ====================================================================
                # STEP 3: SYNTHESIZE MULTIPLE SUMMARIES (if needed)
                # Purpose: If document had multiple chunks, combine summaries into one
                # Creates a final consolidated summary with no redundancy
                # ====================================================================
                if len(summaries) > 1:
                    final_input = "\n\n".join(summaries)
                    final_response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Synthesize the following partial summaries into one final bulleted report (max 300 words). Focus only on primary findings and recommended actions."},
                            {"role": "user", "content": final_input}
                        ]
                    )
                    st.session_state.summary = final_response.choices[0].message.content
                else:
                    # If only one chunk, use its summary directly
                    st.session_state.summary = summaries[0]

            # ====================================================================
            # ERROR HANDLING
            # Purpose: Catch and display specific error types to help users debug
            # ====================================================================
            except Exception as e:
                error_msg = str(e).lower()
                # Check for authentication issues
                if "api_key" in error_msg or "authentication" in error_msg:
                    st.error("❌ Authentication Error: Your API key is invalid.")
                # Check for rate limiting
                elif "rate_limit" in error_msg:
                    st.error("❌ Rate Limit: You've sent too many requests. Please wait a moment.")
                # Generic error handling
                else:
                    st.error(f"❌ Error: {str(e)}")


# ============================================================================
# DISPLAY RESULTS SECTION
# Purpose: Show the generated summary and provide download/clear options
# Only displays if a summary has been generated
# ============================================================================
if st.session_state.summary:
    st.subheader("Summary")
    # Display the summary in markdown format for better formatting
    st.markdown(st.session_state.summary)

    # ========================================================================
    # ACTION BUTTONS (Download & Clear)
    # Purpose: Provide user options to save or reset the summarization
    # ========================================================================
    col1, col2 = st.columns(2)
    
    # Download button: Allows user to save summary as text file
    with col1:
        st.download_button(
            label="Download Summary",
            data=st.session_state.summary,
            file_name="OakTree_Summary.txt",
            mime="text/plain"
        )
    
    # Clear button: Resets the app to allow processing a new document
    with col2:
        if st.button("Clear Results"):
            st.session_state.summary = ""
            # Rerun the app to refresh the UI
            st.rerun()
