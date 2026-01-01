# ResumeAlign - AI CV Reformatter

Transform CVs into standardized formats using AI-powered extraction and custom templates.

## ⚖️ Legal Disclaimer

**IMPORTANT: Please Read Before Use**

ResumeAlign is a **processing tool** that operates on **YOUR uploaded documents only**. 

### Privacy & Data Handling
- ✅ **No data storage**: All processing happens in-memory
- ✅ **No tracking**: We don't collect or store your CVs
- ✅ **Local processing**: Phase 1 & 2 run entirely on the server (no external calls)
- ⚠️ **Phase 3 only**: Uses external AI APIs (Gemini/OpenAI) - review their privacy policies

### Liability Limitations
- ❌ **Not responsible** for content accuracy or AI-generated suggestions
- ❌ **Not legal/tax/career advice**: Use at your own discretion
- ❌ **No warranties**: Provided "AS IS" under MIT License
- ✅ **Educational/Research use**: Designed for HR workflow automation

### Your Responsibilities
- ✅ Ensure you have rights to process uploaded CVs
- ✅ Comply with local data protection laws (GDPR, etc.)
- ✅ Review all AI-generated content before use
- ✅ Don't upload confidential/sensitive data to public deployments

**By using this tool, you acknowledge these terms.**

---

## 🚀 Features

- **Extract Core**: Regex-based CV data extraction (no API needed)
- **Template Sync**: Map CVs to custom Word templates
- **JD Sync**: AI-powered job description matching (optional)

## 📦 Quick Start

### Deploy to Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select this repo → Main file: `dashboard.py`
4. Deploy!

### Local Development

```bash
pip install -r requirements.txt
python start_app.py
```

## 🔑 Configuration

For Phase 3 (JD Sync), add your API key in Streamlit Cloud:
- Settings → Secrets → Add `GEMINI_API_KEY`

## 🛡️ Security Best Practices

- ✅ Use dummy/test CVs for public demos
- ✅ Deploy privately for production use (Streamlit allows password protection)
- ✅ Never commit real client data to Git
- ✅ Review `.gitignore` to exclude sensitive files

## 📄 License

MIT License - Free for commercial use. See [LICENSE](LICENSE) file.

**Legal Precedents**: Similar tools (ResumeParser, CVExpander, OpenResume) have 10K+ stars with zero legal issues.

## 🤝 Support

Built with ❤️ for HR teams worldwide

**Disclaimer**: This is a processing tool, not a legal service. Always verify output and comply with local regulations.
