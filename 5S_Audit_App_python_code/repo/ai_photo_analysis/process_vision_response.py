import json
ticket_id = parameter[1] if len(parameter) > 1 else ''
res = parameter[2] if len(parameter) > 2 else {}

print(f"[5S AI Photo Analysis] LLM Response received: {res}")

if isinstance(res, str):
    try:
        res = json.loads(res)
    except:
        res = {}

has_violation = res.get('has_violation', False)
if has_violation:
    violation = res.get('violation_title', '5S Compliance Violation Detected')
    conf = float(res.get('confidence_score', 88.0))
    if conf <= 1.0:
        conf = round(conf * 100, 1)
    boxes = str(res.get('bounding_boxes', '[]'))
else:
    violation = "No violation detected (Clean & Compliant)"
    conf = float(res.get('confidence_score', 98.5))
    if conf <= 1.0:
        conf = round(conf * 100, 1)
    boxes = "[]"

payload = {
    'ai_detected_violation': violation,
    'ai_confidence_score': conf,
    'ai_bounding_boxes': boxes
}
print(f"[5S AI Photo Analysis] Writing back to Finding Ticket {ticket_id}: {payload}")
output[1] = payload
output[2] = ticket_id
