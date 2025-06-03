from enum import Enum
from Lexical_Analyzer.lexical_analyzer import TokenType, MyToken

class ASTNodeType(Enum):
    let = 1
    fcn_form = 2
    identifier = 3
    integer = 4
    string = 5
    where = 6
    gamma = 7
    lambda_expr = 8
    tau = 9
    rec = 10
    aug = 11
    conditional = 12
    op_or = 13
    op_and = 14
    op_not = 15
    op_compare = 16
    op_plus = 17
    op_minus = 18
    op_neg = 19
    op_mul = 20
    op_div = 21
    op_pow = 22
    at = 23
    true_value = 24  
    false_value = 25
    nil = 26
    dummy = 27
    within = 28
    and_op = 29
    equal = 30
    comma = 31
    empty_params = 32

class ASTNode:
    def __init__(self, node_type, value, children):
        self.type = node_type
        self.value = value
        self.no_of_children = children

class RPALParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.syntax_tree = []
        self.tree_strings = []

    def build_ast(self):
        self.tokens.append(MyToken(TokenType.END_OF_TOKENS, ""))  # Append end marker
        self.parse_expression()  # Begin parsing from root
        if self.tokens[0].type == TokenType.END_OF_TOKENS:
            return self.syntax_tree
        else:
            print("Error: Parsing failed!...........")
            print("TOKENS NOT PROCESSED:")
            for token in self.tokens:
                print("<" + str(token.type) + ", " + token.value + ">")
            return None

    def generate_string_representation(self):
        indentation = ""
        node_stack = []

        while self.syntax_tree:
            if not node_stack:
                if self.syntax_tree[-1].no_of_children == 0:
                    self.append_node_string(indentation, self.syntax_tree.pop())
                else:
                    current_node = self.syntax_tree.pop()
                    node_stack.append(current_node)
            else:
                if self.syntax_tree[-1].no_of_children > 0:
                    current_node = self.syntax_tree.pop()
                    node_stack.append(current_node)
                    indentation += "."
                else:
                    node_stack.append(self.syntax_tree.pop())
                    indentation += "."
                    while node_stack[-1].no_of_children == 0:
                        self.append_node_string(indentation, node_stack.pop())
                        if not node_stack:
                            break
                        indentation = indentation[:-1]
                        current_node = node_stack.pop()
                        current_node.no_of_children -= 1
                        node_stack.append(current_node)

        # Reverse the final list
        self.tree_strings.reverse()
        return self.tree_strings

    def append_node_string(self, indentation, node):
        if node.type in [ASTNodeType.identifier, ASTNodeType.integer, ASTNodeType.string, ASTNodeType.true_value,
                         ASTNodeType.false_value, ASTNodeType.nil, ASTNodeType.dummy]:
            self.tree_strings.append(indentation + node.value)
        elif node.type == ASTNodeType.fcn_form:
            self.tree_strings.append(indentation + "function_form")
        else:
            self.tree_strings.append(indentation + node.value)

    # Main Expression Parsing Methods
                
    # E	->'let' D 'in' E		=> 'let'
    # 	->'fn' Vb+ '.' E		=> 'lambda'
    # 	->Ew;

    def parse_expression(self):
        if self.tokens:  # Check if tokens exist
            current_token = self.tokens[0]
            if hasattr(current_token, 'type') and hasattr(current_token, 'value'):  # Validate token structure
                if current_token.type == TokenType.KEYWORD and current_token.value in ["let", "fn"]:
                    # print('Processing keyword expression...')
                    if current_token.value == "let":
                        # print('Processing let expression...')
                        self.tokens.pop(0)  # Consume "let"
                        self.parse_definition()
                        if self.tokens[0].value != "in":
                            print("Syntax error in expression parsing: 'in' keyword expected")
                        self.tokens.pop(0)  # Consume "in"
                        self.parse_expression()
                        self.syntax_tree.append(ASTNode(ASTNodeType.let, "let", 2))
                    else:
                        self.tokens.pop(0)  # Consume "fn"
                        param_count = 0
                        while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                            self.parse_variable_binding()
                            param_count += 1
                        if self.tokens and self.tokens[0].value != ".":
                            print("Syntax error in expression parsing: '.' expected")
                        if self.tokens:
                            self.tokens.pop(0)  # Consume "."
                            self.parse_expression()
                            self.syntax_tree.append(ASTNode(ASTNodeType.lambda_expr, "lambda", param_count + 1))
                else:
                    # print('Processing standard expression...')
                    self.parse_where_expression()
            else:
                print("Token format is invalid.")
        else:
            print("No tokens available for parsing.")


    # Ew	->T 'where' Dr			=> 'where'
    # 		->T;

    def parse_where_expression(self):
        self.parse_tuple_expression()
        if self.tokens[0].value == "where":
            self.tokens.pop(0)  # Consume "where"
            self.parse_recursive_definition()
            self.syntax_tree.append(ASTNode(ASTNodeType.where, "where", 2))

    # Tuple Expression Parsing

    # T 	-> Ta ( ',' Ta )+ => 'tau'
    # 		-> Ta ;
            
    def parse_tuple_expression(self):
        self.parse_tuple_augment()
        element_count = 1
        while self.tokens[0].value == ",":
            self.tokens.pop(0)  # Consume comma
            self.parse_tuple_augment()
            element_count += 1
        if element_count > 1:
            self.syntax_tree.append(ASTNode(ASTNodeType.tau, "tau", element_count))

    '''
    # Ta 	-> Ta 'aug' Tc => 'aug'
    # 		-> Tc ;
    Left recursion elimination by right recursion conversion
    Ta -> Tc ('aug' Tc)*
    '''
    def parse_tuple_augment(self):
        self.parse_tuple_conditional()
        while self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Consume "aug"
            self.parse_tuple_conditional()
            self.syntax_tree.append(ASTNode(ASTNodeType.aug, "aug", 2))

    '''
    Tc 	-> B '->' Tc '|' Tc => '->'
     		-> B ;
    '''    
    def parse_tuple_conditional(self):
        self.parse_boolean_expression()
        if self.tokens[0].value == "->":
            self.tokens.pop(0)  # Consume '->'
            self.parse_tuple_conditional()
            if self.tokens[0].value != "|":
                print("Syntax error in conditional: '|' separator expected")
                # return
            self.tokens.pop(0)  # Consume '|'
            self.parse_tuple_conditional()
            self.syntax_tree.append(ASTNode(ASTNodeType.conditional, "->", 3))

    # Boolean Expression Parsing Methods
    '''
    # B 	-> B 'or' Bt 	=> 'or'
    #     -> Bt ;	
    
    B -> Bt ('or' Bt)*
    '''
    def parse_boolean_expression(self):
        self.parse_boolean_term()
        while self.tokens[0].value == "or":
            self.tokens.pop(0)  # Consume 'or'
            self.parse_boolean_term()
            self.syntax_tree.append(ASTNode(ASTNodeType.op_or, "or", 2))

    '''
    # Bt	-> Bt '&' Bs => '&'
    # 			-> Bs ;
    
    Bt -> Bs ('&' Bs)*
    '''
    def parse_boolean_term(self):
        self.parse_boolean_secondary()
        while self.tokens[0].value == "&":
            self.tokens.pop(0)  # Consume '&'
            self.parse_boolean_secondary()
            self.syntax_tree.append(ASTNode(ASTNodeType.op_and, "&", 2))

    # Bs	-> 'not' Bp => 'not'
    # 		-> Bp ;

    def parse_boolean_secondary(self):
        if self.tokens[0].value == "not":
            self.tokens.pop(0)  # Consume 'not'
            self.parse_boolean_primary()
            self.syntax_tree.append(ASTNode(ASTNodeType.op_not, "not", 1))
        else:
            self.parse_boolean_primary()

    #  Bp 	-> A ('gr' | '>' ) A => 'gr'
    # 			-> A ('ge' | '>=') A => 'ge'
    # 			-> A ('ls' | '<' ) A => 'ls'
    # 			-> A ('le' | '<=') A => 'le'
    # 			-> A 'eq' A => 'eq'
    # 			-> A 'ne' A => 'ne'
    # 			-> A ;
            

    def parse_boolean_primary(self):
        self.parse_arithmetic_expression()
        current_token = self.tokens[0]
        if current_token.value in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
            self.tokens.pop(0)
            self.parse_arithmetic_expression()
            if current_token.value == ">":
                self.syntax_tree.append(ASTNode(ASTNodeType.op_compare, "gr", 2))
            elif current_token.value == ">=":
                self.syntax_tree.append(ASTNode(ASTNodeType.op_compare, "ge", 2))
            elif current_token.value == "<":
                self.syntax_tree.append(ASTNode(ASTNodeType.op_compare, "ls", 2))
            elif current_token.value == "<=":
                self.syntax_tree.append(ASTNode(ASTNodeType.op_compare, "le", 2))
            else:
                self.syntax_tree.append(ASTNode(ASTNodeType.op_compare, current_token.value, 2))

    # Arithmetic Expression Parsing Methods

    # A 	-> A '+' At => '+'
    # 		-> A '-' At => '-'
    # 		-> '+' At
    # 		-> '-'At =>'neg'
    # 		-> At ;

    def parse_arithmetic_expression(self):
        if self.tokens[0].value == "+":
            self.tokens.pop(0)  # Consume unary plus
            self.parse_arithmetic_term()
        elif self.tokens[0].value == "-":
            self.tokens.pop(0)  # Consume unary minus
            self.parse_arithmetic_term()
            self.syntax_tree.append(ASTNode(ASTNodeType.op_neg, "neg", 1))
        else:
            self.parse_arithmetic_term()

        while self.tokens[0].value in {"+", "-"}:
            operator_token = self.tokens[0]  # Store current operator
            self.tokens.pop(0)  # Consume operator
            self.parse_arithmetic_term()
            if operator_token.value == "+":
                self.syntax_tree.append(ASTNode(ASTNodeType.op_plus, "+", 2))
            else:
                self.syntax_tree.append(ASTNode(ASTNodeType.op_minus, "-", 2))

    '''
    At 	-> At '*' Af => '*'
    				-> At '/' Af => '/'
    				-> Af ;

    At -> Af ('*' Af | '/' Af)*
    '''           
    def parse_arithmetic_term(self):
        self.parse_arithmetic_factor()
        while self.tokens[0].value in {"*", "/"}:
            operator_token = self.tokens[0]  # Store current operator
            self.tokens.pop(0)  # Consume operator
            self.parse_arithmetic_factor()
            if operator_token.value == "*":
                self.syntax_tree.append(ASTNode(ASTNodeType.op_mul, "*", 2))
            else:
                self.syntax_tree.append(ASTNode(ASTNodeType.op_div, "/", 2))

    '''
    Af 	-> Ap '**' Af => '**'
    				-> Ap ;
        
    Af -> Ap ('**' Af)*
    '''

    def parse_arithmetic_factor(self):
        self.parse_arithmetic_power()
        if self.tokens[0].value == "**":
            self.tokens.pop(0)  # Consume power operator
            self.parse_arithmetic_factor()
            self.syntax_tree.append(ASTNode(ASTNodeType.op_pow, "**", 2))

    '''
    Ap 	-> Ap '@' '<IDENTIFIER>' R => '@'
    				-> R ;
    
    Ap -> R ('@' '<IDENTIFIER>' R)*
    '''   
    def parse_arithmetic_power(self):
        self.parse_rator_rand()
        while self.tokens[0].value == "@":
            self.tokens.pop(0)  # Consume @ operator
            
            if self.tokens[0].type != TokenType.IDENTIFIER:
                print("Syntax error in power expression: IDENTIFIER required")
                # Handle parsing error here
                return
            
            self.syntax_tree.append(ASTNode(ASTNodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Consume IDENTIFIER
            
            self.parse_rator_rand()
            self.syntax_tree.append(ASTNode(ASTNodeType.at, "@", 3))

    # Operator and Operand Parsing
    '''
    R 	-> R Rn => 'gamma'
    		-> Rn ;
    
    R -> Rn ('gamma' Rn)*
    '''
            
    def parse_rator_rand(self):
        self.parse_rand()
        while (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
            self.tokens[0].value in ["true", "false", "nil", "dummy"] or
            self.tokens[0].value == "("):
            
            self.parse_rand()
            self.syntax_tree.append(ASTNode(ASTNodeType.gamma, "gamma", 2))

    #        Rn 	-> '<IDENTIFIER>'
    # 				-> '<INTEGER>'
    # 				-> '<STRING>'
    # 				-> 'true' => 'true'
    # 				-> 'false' => 'false'
    # 				-> 'nil' => 'nil'
    # 				-> '(' E ')'
    # 				-> 'dummy' => 'dummy' ;
            
    def parse_rand(self):
        token_type = self.tokens[0].type
        token_value = self.tokens[0].value

        # print(f"Processing token: {token_type}, {token_value}")
        
        if token_type == TokenType.IDENTIFIER:
            self.syntax_tree.append(ASTNode(ASTNodeType.identifier, token_value, 0))
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == TokenType.INTEGER:
            self.syntax_tree.append(ASTNode(ASTNodeType.integer, token_value, 0))
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == TokenType.STRING:
            self.syntax_tree.append(ASTNode(ASTNodeType.string, token_value, 0))
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == TokenType.KEYWORD:
            if token_value == "true":
                self.syntax_tree.append(ASTNode(ASTNodeType.true_value, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "false":
                self.syntax_tree.append(ASTNode(ASTNodeType.false_value, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "nil":
                self.syntax_tree.append(ASTNode(ASTNodeType.nil, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "dummy":
                self.syntax_tree.append(ASTNode(ASTNodeType.dummy, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            else:
                print("Syntax error in operand parsing: Unexpected KEYWORD")
        elif token_type == TokenType.PUNCTUATION:
            if token_value == "(":
                # # print(token_value)
                self.tokens.pop(0)  # Consume '('
                
                self.parse_expression()
                
                if self.tokens[0].value != ")":
                    print("Syntax error in operand parsing: Matching ')' expected")
                    # return
                # # print(tokens[0].value)
                self.tokens.pop(0)  # Consume ')'
            else:
                print("Syntax error in operand parsing: Unexpected PUNCTUATION")
        else:
            print(token_type, token_value)
            print("Syntax error in operand parsing: Expected operand but found something else")

    # Definition Parsing Methods

    # D 	-> Da 'within' D => 'within'
    # 				-> Da ;
            
    def parse_definition(self):
        self.parse_and_definition()
        if self.tokens[0].value == "within":
            # # print(tokens[0].value)
            self.tokens.pop(0)  # Consume 'within'
            self.parse_definition()
            self.syntax_tree.append(ASTNode(ASTNodeType.within, "within", 2))

    # Da  -> Dr ( 'and' Dr )+ => 'and'
    # 					-> Dr ;
            
    def parse_and_definition(self): 
        self.parse_recursive_definition()
        def_count = 1
        while self.tokens[0].value == "and":
            # # print(tokens[0].value)
            self.tokens.pop(0)
            self.parse_recursive_definition()
            def_count += 1
        if def_count > 1:
            self.syntax_tree.append(ASTNode(ASTNodeType.and_op, "and", def_count))

    # Dr  -> 'rec' Db => 'rec'
    # 	-> Db ;
            
    def parse_recursive_definition(self):
        has_rec = False
        if self.tokens[0].value == "rec":
            # # print(tokens[0].value)
            self.tokens.pop(0)
            has_rec = True
        self.parse_basic_definition()
        if has_rec:
            self.syntax_tree.append(ASTNode(ASTNodeType.rec, "rec", 1))

    # Db  -> Vl '=' E => '='
    # 				-> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
    # 				-> '(' D ')' ; 
            
    def parse_basic_definition(self): 
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            self.parse_definition()
            if self.tokens[0].value != ")":
                print("Syntax error in basic definition #1")
                # return
            # print(tokens[0].value)
            self.tokens.pop(0)
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # print(self.tokens[0].value)
            if self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER:
                # Process function form
                self.syntax_tree.append(ASTNode(ASTNodeType.identifier, self.tokens[0].value, 0))
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Consume ID

                child_count = 1  # Identifier child
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    self.parse_variable_binding()
                    child_count += 1
                if self.tokens[0].value != "=":
                    print("Syntax error in basic definition #2")
                    # return
                # print(tokens[0].value)
                self.tokens.pop(0)
                self.parse_expression()

                self.syntax_tree.append(ASTNode(ASTNodeType.fcn_form, "fcn_form", child_count+1))
            elif self.tokens[1].value == "=":
                self.syntax_tree.append(ASTNode(ASTNodeType.identifier, self.tokens[0].value, 0))
                # print(tokens[0].value)
                self.tokens.pop(0)  # Consume identifier
                # print(tokens[0].value)
                self.tokens.pop(0)  # Consume equal
                self.parse_expression()
                self.syntax_tree.append(ASTNode(ASTNodeType.equal, "=", 2))
            elif self.tokens[1].value == ",":
                self.parse_variable_list()
                if self.tokens[0].value != "=":
                    print("Syntax error in basic definition")
                    # return
                # print(tokens[0].value)
                self.tokens.pop(0)
                self.parse_expression()

                self.syntax_tree.append(ASTNode(ASTNodeType.equal, "=", 2))

    # Variable Parsing Methods
                
    # Vb  -> '<IDENTIFIER>'
    # 	  -> '(' Vl ')'
    # 	  -> '(' ')' => '()';

    def parse_variable_binding(self):
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            has_variable_list = False

            if self.tokens[0].type == TokenType.IDENTIFIER:
                # print(self.tokens[0].value)
                self.parse_variable_list()
                has_variable_list = True
            
            if self.tokens[0].value != ")":
                print("Syntax error: unmatched closing parenthesis")
                # return
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            if not has_variable_list:
                self.syntax_tree.append(ASTNode(ASTNodeType.empty_params, "()", 0))
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            self.syntax_tree.append(ASTNode(ASTNodeType.identifier, self.tokens[0].value, 0))
            # print(tokens[0].value)
            self.tokens.pop(0)

    # Vl -> '<IDENTIFIER>' list ',' => ','?;
            
    def parse_variable_list(self):
        var_count = 0
        while True:
            # print(self.tokens[0].value)
            if var_count > 0:
                self.tokens.pop(0)
            if not self.tokens[0].type == TokenType.IDENTIFIER:
                print("Syntax error: identifier expected in variable list")
            # print(self.tokens[0].value)
            self.syntax_tree.append(ASTNode(ASTNodeType.identifier, self.tokens[0].value, 0))
            
            self.tokens.pop(0)
            var_count += 1
            if not self.tokens[0].value == ",":
                break
        
        if var_count > 1:
            self.syntax_tree.append(ASTNode(ASTNodeType.comma, ",", var_count))