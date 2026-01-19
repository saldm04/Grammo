"""Main entry point for the Grammo Compiler.

Handles command-line arguments, parsing, analysis, code generation, and execution.
"""
import sys
import argparse
import logging
from pprint import pprint
from pathlib import Path
from lark import Lark, UnexpectedInput
from .semantic.ast_builder import ASTBuilder
from .semantic.semantic_analyzer import SemanticAnalyzer, SemanticError
from .codegen.code_generator import CodeGenerator
from .codegen.optimizer import GrammoOptimizer
from .codegen.execution import JITExecutor

def load_parser():
    """Loads the Lark parser for Grammo grammar.

    Returns:
        Lark: The initialized Lark parser instance.
    """
    base_dir = Path(__file__).parent
    grammar_path = base_dir / "lex_syntax" / "grammo.lark"
    
    if not grammar_path.exists():
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
    """Main execution entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        stream=sys.stdout
    )

    parser = argparse.ArgumentParser(description="Grammo Compiler and Executor")
    parser.add_argument("file", help="Input Grammo source file (.gm)")
    parser.add_argument("-o", "--output", help="Output path for generated LLVM IR Code")
    parser.add_argument("-O", "--opt-level", type=int, default=3, choices=[0, 1, 2, 3], help="Optimization level (0-3)")
    parser.add_argument("-a", "--ast", action="store_true", help="Print the AST structure to console.")
    
    args = parser.parse_args()

    filename = args.file
    path = Path(filename)
    if not path.exists():
        logging.error(f"File not found: {filename}")
        sys.exit(1)

    logging.info(f"Parsing {filename}...")
    try:
        src = path.read_text(encoding="utf-8")
        parser_inst = load_parser()
        tree = parser_inst.parse(src)
        logging.info("Parsing successful.")

        logging.info("Building AST...")
        builder = ASTBuilder()
        ast_root = builder.transform(tree)
        
        logging.info("Running Semantic Analysis...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast_root)
        logging.info("Semantic Analysis Successful! No errors found.")
        
        if args.ast:
            logging.info("AST Structure:")
            pprint(ast_root)
        
        logging.info("Generating LLVM IR...")
        codegen = CodeGenerator()
        llvm_module = codegen.visit(ast_root)
        
        logging.info(f"Optimizing (Level {args.opt_level})...")
        optimizer = GrammoOptimizer()
        # optimize returns a ModuleRef
        optimized_mod_ref = optimizer.optimize(llvm_module, speed_level=args.opt_level)
        
        if args.output:
            logging.info(f"Writing output to {args.output}...")
            with open(args.output, "w") as f:
                f.write(str(optimized_mod_ref))
                
        logging.info("Executing...")
        executor = JITExecutor()
        executor.run(optimized_mod_ref)

    except UnexpectedInput as e:
        logging.error(f"Syntax Error at line {e.line}, column {e.column}:\n")
        logging.error(e.get_context(src))
        logging.error(str(e))
        sys.exit(1)
    except SemanticError as e:
        logging.error(f"Semantic Error:\n{e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
