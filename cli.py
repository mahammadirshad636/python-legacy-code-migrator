import argparse
import ast
from analyzer.ast_parser import CodeAnalyzer
from analyzer.call_graph import CallGraph
from analyzer.issues import detect_issues
from analyzer.exporter import export_json, export_mermaid
from migration.recommender import recommend
from migration.ai_migrator import migrate_with_ai
from migration.rule_migrator import migrate_rule_based

def analyze_file(path):
    source = open(path, encoding="utf-8").read()
    tree = ast.parse(source)

    analyzer = CodeAnalyzer(path)
    analyzer.visit(tree)

    graph = CallGraph()
    graph.visit(tree)

    issues = detect_issues(source)

    return {
        "file": path,
        "classes": analyzer.classes,
        "functions": analyzer.functions,
        "complex_functions": analyzer.complex_functions,
        "imports": analyzer.imports,
        "calls": graph.calls,
        "issues": issues
    }, source

def main():
    parser = argparse.ArgumentParser("Legacy Code Intelligence CLI")
    parser.add_argument("file", help="Legacy python file")
    parser.add_argument("--ai", action="store_true", help="Use LM Studio AI migration")
    args = parser.parse_args()

    analysis, source = analyze_file(args.file)

    export_json(analysis, "outputs/analysis.json")
    export_mermaid(analysis["calls"], "outputs/callgraph.mmd")

    recommendations = recommend(analysis)
    open("outputs/recommendations.txt", "w").write("\n".join(recommendations))

    if args.ai:
        migrated = migrate_with_ai(source)
    else:
        migrated = migrate_rule_based(source)

    open("outputs/migrated_code.py", "w", encoding="utf-8").write(migrated)

    print("✔ Analysis complete")
    print("✔ analysis.json")
    print("✔ callgraph.mmd")
    print("✔ migrated_code.py")

if __name__ == "__main__":
    main()
