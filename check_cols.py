from docx import Document
from template_engine.template_extractor import iterate_doc_content

doc = Document(r"templates\AM0275 Vishnuraj K J.docx")
content = list(iterate_doc_content(doc))
for i in range(12, 16):
    etype, elem = content[i]
    col_idx = getattr(elem, '_parent_cell_col', -1)
    num_cols = getattr(elem, '_parent_table_cols', -1)
    print(f"Index {i}: txt='{elem.text.strip()}' etype={etype} col={col_idx} cols={num_cols}")
