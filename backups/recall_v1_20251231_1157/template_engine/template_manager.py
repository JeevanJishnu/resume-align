import os
import json
from typing import List, Optional
from .template_models import TemplateSchema
from .template_extractor import extract_template_schema

TEMPLATE_DIR = "templates"
INDEX_FILE = os.path.join(TEMPLATE_DIR, "index.json")

def _load_index() -> List[dict]:
    if not os.path.exists(INDEX_FILE): return []
    try:
        with open(INDEX_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def _save_index(data: List[dict]):
    with open(INDEX_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def register_template(path: str, name: str) -> TemplateSchema:
    schema = extract_template_schema(path, name)
    
    # Update Index
    index = _load_index()
    # Remove existing if overwriting
    index = [i for i in index if i['template_name'] != name]
    
    # Serialize schema
    index.append(schema.dict())
    _save_index(index)
    
    return schema

def get_template_schema(name: str) -> Optional[TemplateSchema]:
    index = _load_index()
    for item in index:
        if item['template_name'] == name:
            return TemplateSchema(**item)
    return None

def list_templates() -> List[str]:
    return [i['template_name'] for i in _load_index()]
