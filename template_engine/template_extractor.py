
import logging
import re
from docx import Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.document import Document as DocClass
from fuzzywuzzy import fuzz
from .template_models import SectionType, TemplateSection, TemplateSchema

logger = logging.getLogger(__name__)

def normalize_text(text):
    if not text: return ""
    return re.sub(r'[\[\]\(\):]', '', text).strip().lower()

def _fuzzy_compare(s1, s2):
    if not s1 or not s2: return False
    return fuzz.ratio(s1, s2) > 85

# Configurable Synonyms
SECTION_SYNONYMS = {
    SectionType.SUMMARY: ["Summary", "Professional Summary", "Profile Summary", "Executive Summary"],
    SectionType.SKILLS: ["Technical Skills", "Key Skills", "Core Competencies", "Skill Highlights", "Skillset", "Skills"],
    SectionType.WORK_EXPERIENCE: ["Work Experience", "Professional Experience", "Employment History", "Experience"],
    SectionType.EDUCATION: ["Education", "Academic Profile", "Educational Background", "Qualification"],
    SectionType.PROJECTS: ["Project Details", "Project Profile", "Project Experience", "Key Projects", "Projects", "Major Projects"],
    SectionType.CERTIFICATIONS: ["Certifications", "Certification Status", "Training", "Achievements"],
    SectionType.TOOLS: ["Tools & Technologies", "Software Tools", "Key Tools"]
}

def iterate_doc_content(doc):
    """
    NUCLEAR TRAVERSAL v3.0:
    Reliably yields all paragraphs and tables in visual order.
    Handles headers, footers, and nested tables.
    """
    yielded_ids = set()

    def _process_container(container, parent_table=None, container_id=None):
        if container_id is None:
            container_id = id(container)

        if hasattr(container, 'element') and hasattr(container.element, 'body'):
            xml_body = container.element.body
        elif hasattr(container, '_element'):
            xml_body = container._element
        else:
            return

        for child in xml_body.iterchildren():
            tag = child.tag
            if tag.endswith('}p'):
                p = Paragraph(child, container if isinstance(container, DocClass) else doc)
                full_id = (container_id, id(p._element))
                if full_id not in yielded_ids:
                    yielded_ids.add(full_id)
                    if parent_table: setattr(p, '_parent_table', parent_table)
                    yield ( 'table_cell' if parent_table else 'para', p)
            elif tag.endswith('}tbl'):
                t = Table(child, container if isinstance(container, DocClass) else doc)
                if id(t._element) not in yielded_ids:
                    yielded_ids.add(id(t._element))
                    yield ('table', t)
                    for row in t.rows:
                        for cell in row.cells:
                            yield from _process_container(cell, parent_table=t, container_id=id(cell))
            elif tag.endswith('}sdt'):
                sdt_content = child.find('.//{http://schemas.microsoft.com/office/word/2006/wordml}sdtContent')
                if sdt_content is not None:
                    class PseudoContainer:
                        def __init__(self, element): self._element = element
                    yield from _process_container(PseudoContainer(sdt_content), parent_table=parent_table, container_id=id(child))

    # 1. Headers/Footers
    for section in doc.sections:
        for h in [section.header, section.first_page_header, section.even_page_header]:
            if h: yield from _process_container(h)
        for f in [section.footer, section.first_page_footer, section.even_page_footer]:
            if f: yield from _process_container(f)
            
    # 2. Body
    yield from _process_container(doc)

def is_section_header(element) -> 'tuple[SectionType, float, bool]':
    if not isinstance(element, Paragraph):
        return SectionType.UNKNOWN, 0.0, False
    text_clean = element.text.strip()
    if not text_clean: return SectionType.UNKNOWN, 0.0, False
    
    # Ignore common field labels within tables
    table_obj = getattr(element, '_parent_table', None)
    is_label_style = False
    if table_obj:
        # If it's in the first column of ANY row in its parent table, it's likely a label
        for row in table_obj.rows:
            if element.text.strip() == row.cells[0].text.strip():
                is_label_style = True
                break
    
    if not is_label_style and text_clean.endswith(':'):
        is_label_style = True
        
    skip_prefixes = [
        "Role:", "Client:", "Tools:", "Environment:", "Technologies:", "Duration:", 
        "Responsibilities:", "Description:", "Category:", "Project Title:", 
        "Technology Stack:", "Tech Stack:", "Company Name:", "Employer:", "Location:"
    ]
    if any(text_clean.lower().startswith(p.lower()) for p in skip_prefixes): 
        return SectionType.UNKNOWN, 0.0, False
    
    label_keywords = ["category", "environment", "technologies", "tools", "responsibilities", "description", "details"]
    if (is_label_style or len(text_clean.split()) <= 2) and text_clean.lower() in label_keywords: 
        return SectionType.UNKNOWN, 0.0, False

    is_placeholder = any(x in text_clean for x in ["{{", "[fill", "[FILL"])
    is_bold = any(run.bold for run in element.runs)
    text_upper = text_clean.upper()
    word_count = len(text_clean.split())
    
    if not is_placeholder and word_count > 6: return SectionType.UNKNOWN, 0.0, False

    # Project Number Match (Project #1, Assignment 1, etc.)
    is_record = False
    if re.search(r"(project|assignment|task|work|experience|employment|job)\s*#?\d+", text_clean.lower()):
        is_record = True
        
    best_type = SectionType.UNKNOWN
    best_score = 0
    
    for stype, synonyms in SECTION_SYNONYMS.items():
        for syn in synonyms:
            if text_clean.lower() == syn.lower():
                # Exact match with top-level synonym means it's NOT a specific record header
                return stype, 1.0, False
            
            score = fuzz.token_set_ratio(text_upper, syn.upper())
            if score > best_score:
                best_score = score
                best_type = stype
            
    if best_score >= 80:
        if is_bold: best_score += 10
        final_score = min(1.0, best_score / 100.0)
        # If it's a good score but also fuzzy matches a record pattern, mark it
        if not is_record and (re.search(r'#\d+|\d+\.', text_clean) or text_clean.endswith(':')):
             is_record = True
        return best_type, final_score, is_record
    
    if is_record:
        # It matched record pattern but maybe not section name exactly
        # If the word 'project' is in it, it's PROJECTS
        if "project" in text_clean.lower(): return SectionType.PROJECTS, 1.0, True
        if "experience" in text_clean.lower() or "work" in text_clean.lower(): return SectionType.WORK_EXPERIENCE, 1.0, True
    
    return SectionType.UNKNOWN, 0.0, False

def _denoise_candidates(candidates: list) -> list:
    if not candidates: return []
    unique_sections = {}
    blacklist = ["role", "client", "duration", "company name", "category", "technologies", "environment", "stack"]
    
    for cand in candidates:
        stype = cand['type']
        t_low = normalize_text(cand['text'])
        if t_low in blacklist: continue
        
        # Keep both top-level and record-level if they appear at different indices
        key = (stype, t_low, cand['is_record'])
        if key not in unique_sections or cand['confidence'] > unique_sections[key]['confidence']:
            unique_sections[key] = cand
            
    return sorted(unique_sections.values(), key=lambda x: x['index'])

def extract_template_schema(template_path: str, template_name: str, doc: Document = None) -> TemplateSchema:
    if doc is None: doc = Document(template_path)
    header_candidates = []
    content_list = list(iterate_doc_content(doc))
    
    for i, (elem_type, element) in enumerate(content_list):
        if elem_type == 'table': continue
        sect_type, score, is_record = is_section_header(element)
        if sect_type != SectionType.UNKNOWN:
            header_candidates.append({
                'index': i, 'type': sect_type, 'confidence': score,
                'text': element.text.strip(), 'elem_type': elem_type,
                'xml_id': id(element._element), 'is_record': is_record
            })
            
    final_list = _denoise_candidates(header_candidates)
    sections = [TemplateSection(
        section_index=c['index'], section_type=c['type'], confidence=c['confidence'],
        header_text=c['text'], raw_heading=c['text'], header_xml_id=c['xml_id'],
        header_element_type=c['elem_type'], is_record_header=c['is_record']
    ) for c in final_list]
    
    logger.info(f"Schema extraction complete for {template_name}: {len(sections)} sections found.")
    return TemplateSchema(template_name=template_name, template_file=template_path, sections=sections)
