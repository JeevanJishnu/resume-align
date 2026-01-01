
from docx import Document
from template_engine.template_extractor import iterate_doc_content, is_section_header
from template_engine.template_models import SectionType

doc = Document('templates/AM0275 Vishnuraj K J.docx')
print(f"Elements in AM0275:")
for etype, elem in iterate_doc_content(doc):
    if etype == 'table':
        print(f"  [TABLE] Rows: {len(elem.rows)}")
        continue
    
    txt = elem.text.strip()
    stype, score = is_section_header(elem)
    if stype != SectionType.UNKNOWN:
        print(f"  [HEADER] {etype}: '{txt}' -> {stype.name} ({score})")
    elif txt:
        print(f"  {etype}: '{txt[:50]}'")
