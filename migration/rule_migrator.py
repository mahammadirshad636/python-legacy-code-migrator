def migrate_rule_based(code):
    code = code.replace("print ", "print(").replace("\n", ")\n")
    code = code.replace("except:", "except Exception:")
    return "# Rule-based migrated code\n\n" + code
