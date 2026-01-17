# def detect_issues(analysis):
#     issues = []
#
#     for name, fn in analysis.get("functions", {}).items():
#         if len(fn.get("args", [])) > 6:
#             issues.append({
#                 "type": "Complexity",
#                 "severity": "MEDIUM",
#                 "message": f"Function '{name}' has too many parameters"
#             })
#
#     for cls, meta in analysis.get("classes", {}).items():
#         if len(meta.get("methods", [])) > 20:
#             issues.append({
#                 "type": "God Class",
#                 "severity": "HIGH",
#                 "message": f"Class '{cls}' has too many methods"
#             })
#
#     return issues

LEGACY_PATTERNS = [
    "frappe.db.sql",
    "eval(",
    "exec(",
    "print("
]

def detect_issues(source):
    issues = []

    for pattern in LEGACY_PATTERNS:
        if pattern in source:
            issues.append(f"Legacy or unsafe usage detected: {pattern}")

    if "except:" in source:
        issues.append("Bare except detected")

    if "global " in source:
        issues.append("Global variable usage")

    return issues
