import json
import logging
from main import preprocess_image, get_cv_segments, extract_name_and_contact, extract_skills_it, extract_work_experience, extract_projects, extract_education, extract_certifications, extract_summary

logging.basicConfig(level=logging.INFO)

def diag():
    cv_path = r"input\20251223_104401_AM0209_Vineetha Thamban .pdf"
    with open(cv_path, "rb") as f:
        content = f.read()
    
    # 1. Extraction
    text = preprocess_image(content, "Vineetha.pdf")
    personal = extract_name_and_contact(content, "Vineetha.pdf")
    segs = get_cv_segments(text)
    
    work_exp = extract_work_experience(segs["experience"])
    companies = [job.get("company", "") for job in work_exp if job.get("company")]
    
    extracted = {
        "full_name": personal["name"],
        "work_experience": work_exp,
        "projects": extract_projects(segs["projects"], companies),
        "education": extract_education(segs["education"]),
        "skills": extract_skills_it(segs["skills"], personal["name"])["skills"]
    }
    
    print("--- Extracted Projects ---")
    print(json.dumps(extracted["projects"], indent=2))
    
    print("\n--- Extracted Work Exp ---")
    print(json.dumps(extracted["work_experience"], indent=2))

if __name__ == "__main__":
    diag()
