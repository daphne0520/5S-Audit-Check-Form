import os
import json

val = parameter[1] if len(parameter) > 1 and isinstance(parameter[1], dict) else {}
ticket_id = parameter[2] if len(parameter) > 2 else ''

print(f"[5S AI Photo Analysis] Raw parameter[1] received from Ticket/Record Created trigger: {json.dumps(val, indent=2)}")

photo_field = val.get('evidence_photo', [])
file_list = []

base_url = os.environ.get('API_BASE_URL') or os.environ.get('BACKEND_URL') or os.environ.get('APP_URL') or 'http://127.0.0.1:8080'
base_url = base_url.rstrip('/')

def resolve_url(item):
    if isinstance(item, dict):
        if item.get('path'):
            p = str(item['path'])
            return p if (p.startswith('http://') or p.startswith('https://')) else (f"{base_url}{p}" if p.startswith('/') else p)
        elif item.get('url'):
            u = str(item['url'])
            return u if (u.startswith('http://') or u.startswith('https://')) else f"{base_url}/{u.lstrip('/')}"
        elif item.get('filename'):
            return f"{base_url}/api/builder/file/{item['filename']}"
        elif item.get('__builder_file_id'):
            return f"{base_url}/api/builder/file/{item['__builder_file_id']}"
    elif isinstance(item, str):
        return item if (item.startswith('http://') or item.startswith('https://')) else f"{base_url}/{item.lstrip('/')}"
    return None

if isinstance(photo_field, list):
    for item in photo_field:
        u = resolve_url(item)
        if u:
            file_list.append(u)
elif isinstance(photo_field, (dict, str)):
    u = resolve_url(photo_field)
    if u:
        file_list.append(u)

print(f"[5S AI Photo Analysis] Resolved {len(file_list)} file payload(s) passed to LLM Vision: {file_list}")
output[1] = file_list if file_list else ""
output[2] = ticket_id
