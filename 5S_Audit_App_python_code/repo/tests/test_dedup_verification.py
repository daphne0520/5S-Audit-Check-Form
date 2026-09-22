import json

# Test scenario simulating 3 successive updates on the same Finding Ticket

def evaluate_flow_if(val, curr_status, prev_status):
    sev = str(val.get('severity_level', ''))
    confirmed = val.get('auditor_confirmed')
    capa_ref = str(val.get('capa_reference_id', '') or '')
    
    # Triple-check dedup logic
    if capa_ref or (curr_status == 'Escalated to CAPA' and prev_status == 'Escalated to CAPA'):
        passed = False
    else:
        is_status_escalated = (curr_status == 'Escalated to CAPA') and (prev_status != 'Escalated to CAPA')
        is_confirmed_high_crit = (curr_status == 'Identified') and (confirmed is True) and (sev in ['High', 'Critical'])
        passed = is_status_escalated or is_confirmed_high_crit
    
    return passed

# Simulation
finding_record = {
    'finding_id': 'FND-TEST-DEDUP-001',
    'parent_audit_id': 'AUD-SESSION-001',
    'severity_level': 'High',
    'auditor_confirmed': True,
    'capa_reference_id': None,
    'category_5s': '1S - Sort'
}

created_capas = []
sent_emails = []

# RUN 1: Initial confirmation of High finding
print("=== SIMULATION STEP 1: Auditor confirms High finding ===")
passed_1 = evaluate_flow_if(finding_record, curr_status='Identified', prev_status='Identified')
print(f"Step 1 Gate Passed: {passed_1}")
if passed_1:
    capa_id = f"CAPA-{finding_record['parent_audit_id']}-{finding_record['finding_id'][:8]}"
    created_capas.append(capa_id)
    sent_emails.append(f"Email sent for {capa_id}")
    # Update finding record to Escalated to CAPA with capa_reference_id
    finding_record['capa_reference_id'] = capa_id
    finding_record_status = 'Escalated to CAPA'
    print(f"Step 1: CAPA created: {capa_id}, Email sent. Finding transitioned to Escalated to CAPA.")

# RUN 2: Status transition event fires (curr_status='Escalated to CAPA', prev_status='Identified')
print("\n=== SIMULATION STEP 2: Transition update event fires ===")
passed_2 = evaluate_flow_if(finding_record, curr_status='Escalated to CAPA', prev_status='Identified')
print(f"Step 2 Gate Passed: {passed_2} (Blocked by capa_reference_id='{finding_record['capa_reference_id']}')")
if passed_2:
    created_capas.append("DUP_CAPA_2")
    sent_emails.append("DUP_EMAIL_2")

# RUN 3: Subsequent field update (e.g. auditor edits notes)
print("\n=== SIMULATION STEP 3: Subsequent field update in Escalated to CAPA ===")
finding_record['notes'] = 'Updated inspection notes after review'
passed_3 = evaluate_flow_if(finding_record, curr_status='Escalated to CAPA', prev_status='Escalated to CAPA')
print(f"Step 3 Gate Passed: {passed_3} (Blocked by status + capa_ref)")
if passed_3:
    created_capas.append("DUP_CAPA_3")
    sent_emails.append("DUP_EMAIL_3")

print(f"\nTotal CAPAs created: {len(created_capas)} ({created_capas})")
print(f"Total Emails sent: {len(sent_emails)} ({sent_emails})")

assert len(created_capas) == 1, f"Expected 1 CAPA, got {len(created_capas)}"
assert len(sent_emails) == 1, f"Expected 1 Email, got {len(sent_emails)}"
output[1] = f"SUCCESS: Exactly 1 CAPA ({created_capas[0]}) and 1 Email created across 3 updates."
