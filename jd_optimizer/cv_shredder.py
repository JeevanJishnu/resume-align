
import json
import re
from .llm_service import LLMService

class CVShredder:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def shred_cv(self, cv_text: str) -> dict:
        """
        Uses the LLM to parse raw CV text into structured JSON.
        """
        if not cv_text or len(cv_text) < 50:
             return {"full_name": "Error: Empty CV Text", "skills": [], "work_experience": [], "projects": []}

        system_prompt = """
You are an expert CV Parser. Your goal is to extract structured data from a raw CV text into a JSON format.
Ignore page headers/footers.

JSON SCHEMA:
{
    "full_name": "Name",
    "email": "email",
    "phone": "phone",
    "linkedin": "url",
    "summary": "Professional Summary",
    "skills": ["List", "Of", "All", "Technical", "Skills"],
    "tools": ["List", "Of", "Tools"],
    "work_experience": [
        {
            "role": "Job Title",
            "company": "Company Name",
            "duration": "Start - End (e.g. Jan 2020 - Present)",
            "location": "City, Country",
            "responsibilities": "Full description of role..."
        }
    ],
    "projects": [
        {
            "title": "Project Name",
            "role": "Role in project",
            "technologies": "Tech Stack",
            "description": "Project details..."
        }
    ],
    "education": [{"degree": "", "institution": "", "duration": ""}],
    "certifications": [{"title": "", "year": ""}]
}

INSTRUCTIONS:
1. Extract ALL work experience items found. Do not summarize or skip older jobs.
2. Extract ALL technical skills found.
3. Ensure "role" is the Job Title (e.g. "Manager") and "company" is the Organization.
4. Output STRICT JSON. No markdown.
"""
        
        user_prompt = f"CV CONTENT:\n{cv_text[:12000]}\n\nOutput JSON:"
        
        response_text = self.llm.call_llm(user_prompt, system_prompt)
        
        try:
            # Clean response if LLM adds markdown backticks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].strip()
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Shredder Error: {e}")
            # Ensure we return a valid dict even on error, to prevent UI crash
            return {
                "full_name": "Analysis Failed",
                "summary": "The AI could not parse this CV. Please try a cleaner PDF.",
                "skills": [],
                "work_experience": [],
                "projects": [],
                "education": []
            }
