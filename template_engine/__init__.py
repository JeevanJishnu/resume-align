"""
Template Engine Package
Handles template extraction, cleaning, and mapping for CV reformatting.
"""

from .template_models import TemplateSchema, TemplateSection, SectionType
from .template_extractor import extract_template_schema
from .template_manager import get_template_schema, register_template, list_templates
from .template_mapper import fill_template

__all__ = [
    'TemplateSchema',
    'TemplateSection', 
    'SectionType',
    'extract_template_schema',
    'get_template_schema',
    'register_template',
    'list_templates',
    'fill_template'
]
