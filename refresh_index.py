from template_engine.template_manager import register_template
import os

templates = [
    ("AM0275", "templates/AM0275 Vishnuraj K J.docx"),
    ("Corp_Dev", "templates/Corp_Dev.docx"),
    ("Fresher_IT", "templates/Fresher_IT.docx"),
    ("Architect", "templates/Architect.docx"),
    ("Service_Company", "templates/Service_Company.docx")
]

print("Refreshing Template Index with Nuclear v4 Logic...")
for name, path in templates:
    if os.path.exists(path):
        print(f"Registering {name}...")
        register_template(path, name)
    else:
        print(f"Skipping {name} (File not found)")

print("Done. Cache Synchronized.")
