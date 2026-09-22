# 5S-Audit-Check-Form
5S methodology is a systematic approach to workplace organization and visual management. It helps manufacturers identify and eliminate waste while improving efficiency, quality, and productivity.

# Problem Statement
5S audits (Sort, Set in Order, Shine, Standardize, Sustain) are one of the most common shop floor compliance checks, but on most sites they still run on paper forms or spreadsheets filled out zone by zone. That makes scoring inconsistent between auditors, evidence easy to lose, and corrective actions hard to trace back to the finding that triggered them. A violation can be logged, "fixed," and closed without anyone confirming the fix actually happened.
This app puts the whole audit lifecycle, zone scan, inspection, AI-assisted detection, auditor confirmation, CAPA assignment, and re-audit verification, on a connected set of status-driven tickets, and uses computer vision to give every auditor a consistent first pass at spotting violations before they apply their own judgment.

# Objective

# Methodology
1. Workflow Automation: Designed and implemented a digital 5S audit lifecycle using the V-ONE low-code development platform. A zone scan opens an Audit ticket, which produces one Finding per pillar, and any confirmed high or critical Finding automatically escalates to a CAPA ticket with a re-audit loop back to the original zone.

2. Zone Identification and Evidence Capture: Each zone is identified by a QR code scanned at the start of inspection, linking the audit session to a fixed zone code so evidence can not be misattributed to the wrong area. Auditors upload photo evidence per pillar directly against the audit session.

3. AI Photo Analysis: Implemented an LLM vision workflow that triggers on evidence upload. A category-scoped prompt evaluates the photo strictly against one pillar at a time, using a constrained output schema so the model returns a violation title, confidence score, bounding box, and severity for each of the five pillars independently rather than one generic result applied across all of them.

4. Auditor Review and Confirmation: AI-detected findings are surfaced to the auditor as a draft, not a final verdict. The auditor confirms, adjusts severity, or dismisses each finding before it is eligible to trigger any downstream escalation, keeping a human decision in the loop for every CAPA that gets raised.

5. CAPA Escalation and Re-Audit: Confirmed high or critical findings automatically create a CAPA ticket, notify the responsible team, and track root cause, containment action, and corrective action through to verification. A re-audit is required to close the loop, and repeated re-audit failures increment a rework counter that escalates to senior management once a threshold is crossed.

6. Scoring: Each pillar is scored on its own scale and rolled up into a zone-level and audit-level compliance score, so a single severe finding in one pillar does not get diluted or hidden inside an overall average.

7. Business Analytics and Dashboard: Developed an executive dashboard covering pillar-level score trends, open finding counts by severity, CAPA turnaround time, re-audit pass rate, and zone-level compliance history, with export support for audit reports.

8. Role-Based Access: Auditors have full access to run audits and view findings. Responsible persons only see and act on the CAPA tickets assigned to them. Management and EHS have read access across audits and findings, with approval rights on CAPA verification.

# Pre-Implementation Findings
1. Inconsistent Manual Scoring 5S audits involve subjective judgment calls across five separate pillars. Paper and spreadsheet based scoring varies significantly between auditors and sites. A structured, pillar-by-pillar digital checklist reduces that variance.

2. Evidence Gets Lost or Disputed Photo evidence taken on personal devices is rarely attached consistently to the finding it supports. Disputes over whether a violation was real or already fixed are hard to resolve without a timestamped record. Tying evidence directly to the ticket at the point of upload closes that gap.

3. Corrective Actions Are Hard to Trace Findings and their corrective actions are often tracked in separate systems or not tracked at all. Without a required verification step, a CAPA can be marked closed without confirming the fix actually worked. A ticket-based workflow with a mandatory re-audit step improves accountability.

4. Not Every Violation Needs the Same Response Low and medium severity findings do not need the same escalation path as high or critical ones. Escalating everything the same way causes alert fatigue and slows down response to what actually matters. Severity-based routing keeps CAPA and notification volume proportional to actual risk.

5. Limited Availability of Production Data The application has not yet been deployed for full production use across all zones. Current data cannot yet establish real defect trends, detection accuracy, or CAPA turnaround benchmarks. Production-level performance should be evaluated after a full audit cycle of real operational data has been collected.

# Future Data Analysis After Implementation
1. Identify the most frequently violated 5S pillar across zones and departments.

2. Monitor finding frequency and severity trends by zone over time.

3. Measure AI detection accuracy against auditor-confirmed findings to tune the confidence threshold.

4. Analyse CAPA turnaround time from escalation to verified closure.

5. Track re-audit pass rate and how often findings require more than one rework cycle.

6. Evaluate audit completion and compliance trends across the site.

7. Compare zone-level and site-level compliance scores before and after app implementation.

## Platform Portability
*The workflow can be adapted to other low-code or enterprise platforms because the core business process is based on status-driven audit, detection, confirmation, escalation, and verification logic rather than platform-specific functionality. The AI vision step is likewise portable to any provider that accepts an image and returns structured output against a defined schema.*
