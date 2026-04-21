# OakTree Report Summarizer - Buildup to AI Project

A collection of Streamlit-based document summarization applications powered by AI. These applications automatically extract text from PDF and Word documents, then use advanced AI models (Google Gemini or OpenAI GPT-4) to generate concise, professional summaries.

---

## Project Overview

This project demonstrates a progression of implementations for automated document summarization, starting from basic Gemini integration and evolving toward production-ready code with OpenAI integration. Each application follows the same core concept: upload a business document and receive an AI-generated summary under 300 words that highlights key findings and recommended actions.

---

## Applications

### 1. **app.py** - Basic Gemini Summarizer
A foundational Streamlit application using Google's Generative AI (Gemini 2.5 Flash).

**Key Features:**
- Extracts text from PDF and DOCX files
- Requires user to input their own Google API key
- Generates bulleted summaries of business reports
- Lightweight and fast

**How It Works:**
1. User enters their Google API key in the password field
2. Uploads a PDF or DOCX file
3. Clicks "Summarize with OakTree" button
4. Displays summary on screen

**Best For:** Developers testing Gemini API functionality

---

### 2. **app2.py** - Improved Gemini Summarizer
An enhanced version of app.py with better system instructions and session state management.

**Key Features:**
- Uses system instructions to enforce consistent output format
- Stores summary in Streamlit session state
- Includes "Download Summary" button to export results as text file
- "Clear Results" button to reset the app
- Hardcoded API key for testing (⚠️ Not recommended for production)

**Improvements Over app.py:**
- Better error handling and user feedback
- Download functionality for summaries
- Cleaner UI with action buttons
- Session state prevents data loss on page refresh

**Best For:** Teams with shared API keys in secure environments

---

### 3. **app3.py** - Production-Ready OpenAI Summarizer
A production-grade application using OpenAI's GPT-4 model with security best practices.

**Key Features:**
- Uses OpenAI API instead of Google Gemini
- Implements proper security: accepts API key from Streamlit secrets or sidebar
- Lower temperature setting (0.3) for focused, professional output
- Caching to avoid re-extracting text on page reruns
- Comprehensive error handling

**How It Works:**
1. Reads API key from `secrets.toml` or sidebar input
2. Extracts text from uploaded file
3. Sends to GPT-4 with professional summarization prompt
4. Stores result in session state
5. Provides download and clear buttons

**Best For:** Production deployments and enterprise use

---

### 4. **openai-app3.py** - Advanced OpenAI Summarizer with Text Chunking
The most sophisticated version with enhanced code organization and large document support.

**Key Features:**
- **Text Chunking:** Automatically breaks large documents into smaller chunks to avoid OpenAI token limits
- **Organized Code:** Clear sections with detailed comments for maintainability
- **Sidebar Configuration:** Keeps main interface clean
- **Robust Error Handling:** Comprehensive try-catch blocks
- **Improved UX:** Spinner feedback during processing
- **Professional Settings:** Lower temperature (0.3) for consistent output

**Key Function - `chunk_text()`:**
Splits documents larger than 12,000 characters into manageable chunks to prevent API token overflow errors.

**Best For:** Processing large business documents and reports

---

## How to Use

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- API key from either Google (for app.py/app2.py) or OpenAI (for app3.py/openai-app3.py)

### Installation

1. **Clone or download the repository:**
   ```bash
   cd /path/to/Buildup
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running an Application

Choose which app version to run:

**For Gemini versions (app.py or app2.py):**
```bash
streamlit run app.py
```

**For OpenAI versions (app3.py or openai-app3.py):**
```bash
streamlit run openai-app3.py
```

The app will open in your browser at `http://localhost:8501`

---

## Configuration

### Getting API Keys

**Google Gemini API:**
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create new API key
4. Copy and paste into app

**OpenAI API:**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Go to API keys section
3. Create new secret key
4. Copy and paste into app or `secrets.toml`

### Using Secrets (Recommended for Production)

Create `.streamlit/secrets.toml` in your project:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

Streamlit will automatically load this file without exposing the key in code.

---

## Dependencies

The project uses the following key Python libraries:

| Library | Purpose |
|---------|---------|
| `streamlit` | Web application framework for building interactive UIs |
| `openai` | OpenAI API client (for GPT-4 integration) |
| `google-generativeai` | Google Gemini API client |
| `pypdf` | Extract text from PDF files |
| `python-docx` | Extract text from Word documents (.docx) |
| `pandas` | Data manipulation and analysis |

See `requirements.txt` for complete dependency list.

---

## Summarization Process

All applications follow this workflow:

1. **Input:** User uploads PDF or DOCX file
2. **Extraction:** Text is extracted from document
3. **Chunking:** Large documents split into sections (openai-app3.py only)
4. **Prompt:** Document text sent to AI with professional summarization instructions
5. **Processing:** AI generates 300-word maximum summary
6. **Output:** Summary displayed and available for download

### Summarization Instructions

The AI is instructed to:
- Act as a professional technical analyst
- Focus on primary findings and recommended actions only
- Avoid introductory filler or unnecessary details
- Format output as clean bullet points
- Keep total length under 300 words

---

## Which Version Should I Use?

| Use Case | Recommended App |
|----------|-----------------|
| Learning / Testing | `app.py` |
| Team with shared API keys | `app2.py` |
| Production with OpenAI | `app3.py` |
| Large documents | `openai-app3.py` |

---

## Troubleshooting

**"API key is invalid"**
- Verify your API key is correct
- Ensure you're using the right API key for the selected service (Google vs. OpenAI)
- Check that your API key has necessary permissions enabled

**"Error reading file"**
- Ensure file is valid PDF or DOCX format
- Try re-exporting the file from its original application
- Check file size (very large files may timeout)

**"Token limit exceeded"** (OpenAI versions)
- Use `openai-app3.py` which includes text chunking
- Or upload a shorter document

---

## File Structure

```
Buildup/
├── app.py                    # Basic Gemini implementation
├── app2.py                   # Improved Gemini with session state
├── app3.py                   # Production OpenAI implementation
├── openai-app3.py            # Advanced OpenAI with chunking
├── requirements.txt          # Python dependencies
├── api.txt                   # API keys and prompts (reference only)
└── README.md                 # This file
```

---

## Security Notes

- **Never commit API keys** to version control
- Use `secrets.toml` for local development
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage for unauthorized access

---

## Future Improvements

Potential enhancements to explore:
- Multi-language summarization support
- Custom summarization templates
- Batch processing for multiple documents
- Export to various formats (PDF, Word, Markdown)
- Summary history and tracking
- Adjustable summary length and detail level

---

## License

This project is part of the Buildup to AI learning initiative.
