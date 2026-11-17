# LPU Placement & Career Chatbot (Streamlit)

A Streamlit-based Q&A chatbot powered by Groq that answers student queries strictly based on the LPU Career Services & Placement Policy Guide.

## Project Structure

```text
lpu_placement_chatbot/
├── .streamlit/
│   ├── config.toml       # UI theme and server settings
│   └── secrets.toml      # API key configuration (keep private!)
├── .gitignore
├── app.py                # Main Streamlit application
├── README.md
└── requirements.txt      # Python dependencies
```

## Setup & Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify API Key:**
   Open `.streamlit/secrets.toml` and ensure `GROQ_API_KEY` is set.

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
