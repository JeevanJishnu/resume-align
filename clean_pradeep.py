
import logging
from docx import Document
from template_engine.template_cleaner import clean_template_content
from template_engine.template_extractor import extract_template_schema

logging.basicConfig(level=logging.INFO)

input_path = 'templates/Pradeep_Kumar_P_C_Snowflake_Dev_10yr_exp_OB_Format 1.docx'
output_path = 'templates/Pradeep_Cleaned.docx'

print(f"Cleaning {input_path}...")
doc = Document(input_path)
schema = extract_template_schema(input_path, "Pradeep")
clean_template_content(doc, schema)
doc.save(output_path)
print(f"Saved cleaned template to {output_path}")
