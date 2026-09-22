import json

val = parameter[1] if len(parameter) > 1 and isinstance(parameter[1], dict) else {}
finding_rec_id = str(parameter[2]) if len(parameter) > 2 and parameter[2] else ''
finding_id = str(val.get('finding_id', '')) or 'FND-AUTO'

print(f"[CAPA Escalation] Triggered for Finding {finding_id} (Record {finding_rec_id})")

# State persistence across execution cycles via internal_memory
global internal_memory
if 'internal_memory' not in globals() or not isinstance(internal_memory, set):
    internal_memory = set()

capa_ref = str(val.get('capa_reference_id', '') or '')
capa_exists = bool(capa_ref) or (finding_id in internal_memory)

if not capa_exists:
    internal_memory.add(finding_id)
    rework = int(val.get('rework_counter', 0))
    is_escalated_review = rework >= 3
    audit_id = str(val.get('parent_audit_id', 'AUD-SESSION'))
    severity = str(val.get('severity_level', 'High'))
    category = str(val.get('category_5s', '5S Finding'))
    capa_id = f"CAPA-{audit_id}-{finding_id[:8]}"

    print(f"[CAPA Escalation] Generating CAPA Ticket & Notification for finding {finding_id} (Audit {audit_id}, Severity {severity})")

    # output[1]: CAPA Ticket creation payload
    output[1] = {
        'capa_id': capa_id,
        'source_finding_id': finding_id,
        'source_audit_id': audit_id,
        'severity': severity,
        'target_due_date': '2026-08-30',
        'rework_counter': rework,
        'escalated_for_review': is_escalated_review
    }

    # output[2]: Email recipient
    output[2] = "ehs-team@vitrox.com"

    # output[3]: Email subject
    output[3] = f"🚨 [Action Required] 5S Audit Violation Escalated to CAPA - Audit {audit_id}"

    # output[4]: Email body
    output[4] = f"""Dear 5S Team & Area Supervisor,

A 5S audit violation has been identified and escalated to CAPA:

• Audit Reference: {audit_id}
• Finding ID: {finding_id}
• Severity: {severity}
• Status: Awaiting CAPA Resubmission

Please access the CAPA Action & Verification page to submit the required containment actions and root-cause verification.

Regards,
5S Smart Audit Automated System"""

    # output[5]: Finding Ticket Record ID for update
    output[5] = finding_rec_id

    # output[6]: Finding Ticket update payload (transition to Escalated to CAPA with capa_reference_id)
    output[6] = {
        'finding_id': finding_id,
        'parent_audit_id': audit_id,
        'category_5s': category,
        'severity_level': severity,
        'capa_reference_id': capa_id,
        'notes': f"Auto-escalated to CAPA ({capa_id}) on {severity} severity finding."
    }
else:
    print(f"[CAPA Escalation] Finding {finding_id} already has CAPA record ({capa_ref}). Skipping duplicate alert.")
