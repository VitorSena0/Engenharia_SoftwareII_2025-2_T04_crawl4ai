import ast
import os
import sys

#esse script percorre arquivos .py em um diretório, analisa a AST (estrutura de sintaxe) dos arquivos para extrair classes, métodos e funções de nível de módulo, e gera um diagrama no formato Mermaid (classDiagram) representando as classes, seus métodos, heranças e as funções livres agrupadas.

def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    classes = []
    functions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            bases = [b.id if isinstance(b, ast.Name) else getattr(b, 'attr', '?') for b in node.bases]
            classes.append({"name": node.name, "methods": methods, "bases": bases})
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    return classes, functions

def walk_dir(root):
    all_classes = []
    all_functions = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py"):
                path = os.path.join(dirpath, fn)
                try:
                    cls, funcs = parse_file(path)
                    all_classes.extend(cls)
                    all_functions.extend(funcs)
                except Exception as e:
                    print(f"Warning: failed to parse {path}: {e}", file=sys.stderr)
    return all_classes, all_functions

def to_mermaid(classes, functions, title=None):
    lines = []
    lines.append("classDiagram")
    if title:
        lines.append(f"%% {title}")
    # classes
    for c in classes:
        # attributes omitted for simplicity; list methods
        if c["methods"]:
            methods_text = "\\n".join([f"+{m}()" for m in c["methods"]])
            lines.append(f'class {c["name"]} {{\n  {methods_text}\n}}')
        else:
            lines.append(f"class {c['name']}")
    # inheritance
    for c in classes:
        for b in c["bases"]:
            if b: lines.append(f"{b} <|-- {c['name']}")
    # free functions as a module-like class
    if functions:
        lines.append("class FreeFunctions {")
        for f in functions:
            lines.append(f"  +{f}()")
        lines.append("}")
    return "\n".join(lines)
    
    if __name__ == "__main__":
        root = sys.argv[1] if len(sys.argv) > 1 else "."
        classes, functions = walk_dir(root)
        mermaid = to_mermaid(classes, functions, title=f"Diagrama gerado de {root}")
    print(mermaid)
