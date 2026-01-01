
import json
from .llm_service import LLMService

SYSTEM_PROMPT = """
You are a JD Match Optimizer Expert. Your task is to analyze a candidate's CV (in JSON format) against a Job Description (JD).

Calculations:
1. Technical Match Score (0-100%): Match between skills/tools in CV vs JD.
2. Experience Match Score (0-100%): Match between work history/roles vs JD requirements.
3. Overall Match Score (0-100%): Average of above + alignment with summary/goals.

Suggestions:
Provide specific, actionable suggestions to improve the score to the TARGET SCORE provided by the user.
Suggestions can be:
- "Add": New content to add (Skills, bullet points).
- "Modify": Content to paraphrase or tweak for better alignment.
- "Rewrite": Entire sections that need a more impactful narrative.

You MUST return strictly valid JSON with the following structure:
{
    "scores": {
        "technical": 85,
        "experience": 70,
        "overall": 78
    },
    "analysis": "Brief qualitative summary of the fit.",
    "missing_keywords": ["keyword1", "keyword2"],
    "suggestions": [
        {
            "section": "summary",
            "type": "Modify",
            "original_text": "...",
            "suggested_text": "...",
            "reason": "..."
        },
        {
            "section": "skills",
            "type": "Add",
            "suggested_text": "Skill Name",
            "reason": "Mentioned in JD as requirement."
        }
    ]
}
"""

class JDOptimizer:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def analyze_match(self, cv_json, jd_text, target_score=85):
        user_prompt = f"""
TARGET SCORE: {target_score}%
JOB DESCRIPTION:
{jd_text}

CANDIDATE CV (JSON):
{json.dumps(cv_json, indent=2)}

Analyze the fit and provide suggestions to reach the target score. Use JSON format.
"""
        response_text = self.llm.call_llm(user_prompt, SYSTEM_PROMPT)
        try:
            # Clean response if LLM adds markdown backticks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].strip()
            
            return json.loads(response_text)
        except Exception as e:
            return {"error": f"Failed to parse LLM response: {str(e)}", "raw": response_text}

    def apply_optimizations(self, cv_json, selected_suggestions, edit_mode="tweak"):
        """
        Applies selected suggestions to the CV JSON.
        edit_mode: 'tweak' (paraphrasing/minor) or 'rewrite' (full AI rewrite)
        """
        optimized_cv = json.loads(json.dumps(cv_json)) # Deep copy
        
        for sug in selected_suggestions:
            section = sug.get("section", "").lower()
            new_text = sug.get("suggested_text", "")
            
            if section == "summary":
                optimized_cv["summary"] = new_text
            elif section == "skills":
                if new_text not in optimized_cv.get("skills", []):
                    optimized_cv.setdefault("skills", []).append(new_text)
            elif section == "tools":
                 if new_text not in optimized_cv.get("tools", []):
                    optimized_cv.setdefault("tools", []).append(new_text)
            # Add logic for experience/projects text replacement
            elif section in ["work_experience", "projects", "experience"]:
                # Map 'experience' to 'work_experience'
                target_key = "work_experience" if "experience" in section else "projects"
                items = optimized_cv.get(target_key, [])
                
                # If we have original_text, try to find the item containing it
                orig_snippet = sug.get("original_text", "")[:50] # Check first 50 chars match
                
                matched = False
                if orig_snippet:
                    for item in items:
                        # Check description/responsibilities for match
                        desc = item.get("description", item.get("responsibilities", ""))
                        if orig_snippet in desc or getattr(desc, "startswith", lambda x: False)(orig_snippet):
                            if "experience" in section:
                                item["responsibilities"] = new_text
                            else:
                                item["description"] = new_text
                            matched = True
                            break
                            
                # If no match but it's an "Add", append new item? 
                # Or if it's a general suggestion without specific target, we might skip or append.
                if not matched and sug.get("type", "").lower() == "add":
                    # Create a generic new item
                    new_item = {
                        "role": "New Role" if target_key == "work_experience" else "New Project",
                        "company": "N/A",
                        "duration": "N/A",
                        "responsibilities" if target_key == "work_experience" else "description": new_text
                    }
                    items.insert(0, new_item) # Add to top
                    
            elif section == "certifications":
                optimized_cv.setdefault("certifications", []).append({"title": new_text})

        return optimized_cv
