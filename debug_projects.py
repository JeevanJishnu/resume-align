
import json
from main import get_cv_segments, extract_projects

with open('process_vineetha.py', 'r', encoding='utf-8') as f:
    content = f.read()
    cv_text = content.split('CV_TEXT = """')[1].split('"""')[0]

segs = get_cv_segments(cv_text)
projects = extract_projects(segs.get('projects', ''), [])

print(f"Num Projects: {len(projects)}")
for i, p in enumerate(projects):
    print(f"\nProject #{i+1}:")
    print(json.dumps(p, indent=2))
