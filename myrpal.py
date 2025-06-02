import argparse
import tokenize
from Lexical_Analyzer.lexical_analyzer import tokenize, show_tokens

def main():
    parser = argparse.ArgumentParser(description='Run and debug RPAL programs.')
    parser.add_argument('file_name', type=str, help='Path to the RPAL source file')
    parser.add_argument('-ast', action='store_true', help='Show abstract syntax tree')
    parser.add_argument('-sast', action='store_true', help='Show standardized abstract syntax tree')

    args = parser.parse_args()

    input_file = open(args.file_name, "r")
    input_text = input_file.read()
    input_file.close()

    show_tokens(tokenize(input_text))

    if args.ast:
        print('Make AST here')

if __name__ == "__main__":
    main()
