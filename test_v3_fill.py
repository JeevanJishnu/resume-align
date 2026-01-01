from jd_optimizer.core.template_mapper import fill_template
from jd_optimizer.core.template_models import TemplateSchema, TemplateSection, SectionType
import os
import json

# Dummy Schema
template_path = "templates/Extractor_Master.docx"
output_path = "debug_v3_output.docx"

# Helper to verify file exists
if not os.path.exists(template_path):
    print(f"ERROR: Template {template_path} not found!")
    exit(1)

schema = TemplateSchema(
    template_name="Debug",
    template_file=template_path,
    sections=[] # Empty list satisfies validation even if not useful
)

# Dummy Data
data = {
    "full_name": "John Doe",
    "email": "john@example.com",
    "projects": [
        {"title": "Project A", "duration": "2023"},
        {"title": "Project B", "duration": "2022"}
    ],
    "work_experience": [],
    "education": [],
    "skills": ["Python", "Streamlit"]
}

print("Running fill_template...")
try:
    fill_template(schema, data, output_path)
    print("Success! Output created.")
except Exception as e:
    print(f"FAILED: {e}")
