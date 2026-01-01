
from docx import Document
from template_engine.template_extractor import iterate_doc_content, is_section_header
from template_engine.template_models import SectionType

doc = Document('templates/AM0275 Vishnuraj K J.docx')
print("Inspecting template sections...")

current_sect = SectionType.UNKNOWN
for etype, elem in iterate_doc_content(doc):
    stype, score = is_section_header(elem)
    if stype != SectionType.UNKNOWN and score >= 0.7:
        current_sect = stype
        print(f"\n[SECTION HEADER] {current_sect.name} (Score: {score:.2f}) -> Text: '{elem.text.strip()}'")
    else:
        # Check if it would be a target for the current section
        print(f"  [TARGET?] Current: {current_sect.name} | Text: '{elem.text[:30].strip()}...'")
