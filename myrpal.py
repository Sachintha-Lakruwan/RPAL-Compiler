import argparse
import tokenize
from Lexical_Analyzer.lexical_analyzer import tokenize, show_tokens
from Parser.parser import RPALParser

def main():
    parser = argparse.ArgumentParser(description='Run RPAL programs.')
    parser.add_argument('file_name', type=str, help='Path to the RPAL source file')
    parser.add_argument('-ast', action='store_true', help='Show abstract syntax tree')
    parser.add_argument('-sast', action='store_true', help='Show standardized abstract syntax tree')

    args = parser.parse_args()

    input_file = open(args.file_name, "r")
    input_text = input_file.read()
    input_file.close()

    tokens = tokenize(input_text)

    parser = RPALParser(tokens)
    ast_nodes = parser.build_ast()
    if ast_nodes is None:
        return
    
    # Abstract Syntax Tree (AST)
    string_ast = parser.generate_string_representation()
    if args.ast:
        for string in string_ast:
            print(string)
        return

if __name__ == "__main__":
    main()
