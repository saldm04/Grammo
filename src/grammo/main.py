import sys
from pathlib import Path
from lark import Lark, UnexpectedInput
from .semantic.ast_builder import ASTBuilder
from .semantic.semantic_analyzer import SemanticAnalyzer, SemanticError

def load_parser():
    # Grammar is in lex_syntax/grammo.lark relative to src/grammo/
    base_dir = Path(__file__).parent
    grammar_path = base_dir / "lex_syntax" / "grammo.lark"
    
    if not grammar_path.exists():
        # Fallback if running layout is different
        grammar_path = Path("grammo.lark")
    
    if not grammar_path.exists():
        print(f"Error: Could not find grammar at {grammar_path.absolute()}")
        sys.exit(1)

    with open(grammar_path, "r", encoding="utf-8") as f:
        grammar = f.read()

    parser = Lark(
        grammar,
        start="start",
        parser="lalr",
        propagate_positions=True,
        maybe_placeholders=False,
    )
    return parser

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m grammo.main <file.gm>")
        sys.exit(1)

    filename = sys.argv[1]
    path = Path(filename)
    if not path.exists():
        print(f"Error: File not found: {filename}")
        sys.exit(1)

    print(f"Parsing {filename}...")
    try:
        src = path.read_text(encoding="utf-8")
        parser = load_parser()
        tree = parser.parse(src)
        print("Parsing successful.")

        print("Building AST...")
        builder = ASTBuilder()
        ast_root = builder.transform(tree)
        
        print("Running Semantic Analysis...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast_root)
        
        print("Semantic Analysis Successful! No errors found.")
        
        # Optional: Print Symbol Table summary?
        # print("Global Symbols:", analyzer.symbol_table.scopes[0].keys())

    except UnexpectedInput as e:
        print(f"Syntax Error at line {e.line}, column {e.column}:\n")
        print(e.get_context(src))
        print(e)
        sys.exit(1)
    except SemanticError as e:
        print(f"Semantic Error:\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
