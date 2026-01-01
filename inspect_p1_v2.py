
from docx import Document
from template_engine.template_extractor import iterate_doc_content

doc = Document('templates/Pradeep_Kumar_P_C_Snowflake_Dev_10yr_exp_OB_Format 1.docx')
found = False
for etype, elem in iterate_doc_content(doc):
    txt = elem.text.strip()
    if 'Project #1' in txt: 
        found = True
        print(f"FOUND PROJECT #1: {etype}")
    if found:
        print(f"  {etype}: {repr(txt[:100])}")
    if 'Project #2' in txt: break
