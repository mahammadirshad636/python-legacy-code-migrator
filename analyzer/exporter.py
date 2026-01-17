import json

def export_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def export_mermaid(calls, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("graph TD\n")
        for c in calls:
            f.write(f"    A --> {c}\n")
