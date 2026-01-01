# ResumeAlign - AI CV Reformatter

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Google Gemini API Key (free tier available at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Main file: `dashboard.py`
   - Click "Deploy"

3. **Configure Secrets** (Optional)
   - In Streamlit Cloud dashboard, go to "Advanced settings" → "Secrets"
   - Add your Gemini API key:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```

### Features

**Phase 1: Extract Core**
- Upload any CV (PDF)
- Automatically extracts structured data using regex
- Downloads formatted Word document

**Phase 2: Template Sync**
- Upload custom Word templates
- Map CV data to your brand's design
- Perfect for HR teams with specific layouts

**Phase 3: JD Sync** (Requires API Key)
- AI-powered JD matching
- Optimization suggestions
- Supports Gemini/OpenAI/Groq

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python start_app.py
```

### Architecture

- **Serverless**: No backend required, runs entirely in Streamlit
- **Regex-based extraction**: Fast, no AI costs for Phase 1 & 2
- **Optional AI**: Phase 3 uses external APIs only when needed

### Notes

- Phase 1 & 2 work offline (no API calls)
- Phase 3 requires internet + API key
- All processing happens server-side (secure)
- Templates stored in `templates/` directory
