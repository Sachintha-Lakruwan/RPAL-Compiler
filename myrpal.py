import argparse
import tokenize
from Lexical_Analyzer.lexical_analyzer import tokenize, show_tokens
from Parser.parser import RPALParser
from Standardizer.standaradizer import build_tree, standardize_tree, print_tree
from CSE_Machine.control_structures import ControlStructureGenerator
from CSE_Machine.cseMachine import CSEMachine

def main():
    parser = argparse.ArgumentParser(description='Run RPAL programs.')
    parser.add_argument('file_name', type=str, help='Path to the RPAL source file')
    parser.add_argument('-tokens', action='store_true', help='Show tokens')
    parser.add_argument('-ast', action='store_true', help='Show abstract syntax tree')
    parser.add_argument('-sast', action='store_true', help='Show standardized abstract syntax tree')
    parser.add_argument('-cs', action='store_true', help='Show control structures')

    args = parser.parse_args()

    input_file = open(args.file_name, "r")
    input_text = input_file.read()
    input_file.close()

    # Lexical Analyzer
    tokens = tokenize(input_text)
    
    if args.tokens:
        show_tokens(tokens)
        return
    
    # Abstract Syntax Tree (AST)
    parser = RPALParser(tokens)
    ast_nodes = parser.build_ast()
    if ast_nodes is None:
        return

    string_ast_list = parser.generate_string_representation()
    string_ast = ""
    for string in string_ast_list:
        string_ast += string + "\n"

    if args.ast:
        print(string_ast)
        return

    # Standard Abstract Syntax Tree (SAST)
    tree_root = build_tree(string_ast)
    standardized_root = standardize_tree(tree_root.children[0])

    if args.sast:
        print_tree(standardized_root)
        return
    
    # Generate control structures
    generator = ControlStructureGenerator()
    control_structures = generator.generate(standardized_root)

    if args.cs:
        for name, items in control_structures.items():
            print(f"{name} = {' '.join(items)}")
        return
    
    machine = CSEMachine(control_structures)
    
    # Initial state: Stack has e0, Control has e0, delta0
    machine.stack = ["e0"]
    machine.control = ["e0", "delta0"]
    
    result = machine.run()
    print(f"\nFinal result: {result}")

if __name__ == "__main__":
    main()
