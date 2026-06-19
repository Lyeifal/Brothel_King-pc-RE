#!/usr/bin/env python3
"""Export perform_job_dict from jobs.rpy to JSON."""
import ast
import json
import sys

SRC = "game/core/data/jobs.rpy"
DST = "game/core/data/jobs/perform_job_dict.json"


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the dict assignment
    start = content.find("perform_job_dict = {")
    if start == -1:
        print("ERROR: Could not find perform_job_dict assignment")
        sys.exit(1)

    # Find the matching closing brace (last one before trailing whitespace)
    # The dict ends at the last '}' before the file ends
    end = content.rfind("}")
    if end == -1 or end < start:
        print("ERROR: Could not find closing brace")
        sys.exit(1)

    dict_text = content[start:end + 1]

    # Parse as AST
    tree = ast.parse(dict_text)

    # Replace __("string") with "string" in AST
    class UnwrapTranslator(ast.NodeTransformer):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "__":
                # Replace Call with its first argument (the string)
                if node.args:
                    return self.visit(node.args[0])
            # Continue visiting children but return original node type
            return self.generic_visit(node)

    transformer = UnwrapTranslator()
    tree = transformer.visit(tree)

    # Compile and execute in isolated namespace
    code = compile(tree, "<jobs_dict>", "exec")
    namespace = {}
    exec(code, namespace)
    perform_job_dict = namespace["perform_job_dict"]

    # Serialize to JSON (tuples become lists, which is fine)
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(perform_job_dict, f, ensure_ascii=False, indent=2, default=list)

    print(f"Exported {len(perform_job_dict)} entries to {DST}")

    # Verify round-trip: load and compare
    with open(DST, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    if len(loaded) != len(perform_job_dict):
        print("ERROR: Round-trip size mismatch")
        sys.exit(1)

    print("Round-trip verification OK")


if __name__ == "__main__":
    main()
