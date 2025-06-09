class CSEMachine:
    def __init__(self, control_structures):
        self.control = []  # Control stack (LIFO - rightmost element is popped first)
        self.stack = []    # Stack (LIFO)
        self.environments = {"e0": {}}  # Environment storage
        self.env_counter = 0  # To generate new environment names
        
        self.deltas = control_structures
        
        self.builtins = {
            # Existing builtins
            "Print": self._builtin_print,
            "Order": self._builtin_order,
            "eq": self._builtin_eq,
            
            # Truth value operations
            "or": self._builtin_or,
            "not": self._builtin_not,
            "ne": self._builtin_ne,
            
            # Integer operations (additional ones)
            "**": self._builtin_power,
            "ls": self._builtin_ls,
            "gr": self._builtin_gr,
            "le": self._builtin_le,
            "ge": self._builtin_ge,
            "neg": self._builtin_neg,  # NEW: Negation operation
            
            # String operations
            "Stem": self._builtin_stem,
            "Stern": self._builtin_stern,
            "Conc": self._builtin_conc,
        }
        
        # Binary operators (updated with new ones)
        self.binary_operators = {
            '+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '˜', '|',
            '!', '#', '%', 'ˆ', '_', '[', ']', '{', '}', '"', "'", '?',
            '**', 'eq', 'ne', 'ls', 'gr', 'le', 'ge', 'or', 'not'
        }
        
        # Unary operators
        self.unary_operators = {
            'neg', 'not'  # neg is unary, not can be both unary and binary
        }
    
    def _builtin_print(self, value):
        print(f"Output: {value}")
        return value
    
    def _builtin_order(self, value):
        """Returns the length/order of a tuple"""
        if isinstance(value, str):
            # Handle tuple representation like "(1, 2, 3, 4, 5)"
            if value.startswith('(') and value.endswith(')'):
                inner = value[1:-1].strip()
                if inner == "":
                    return 0  # Empty tuple
                # Count comma-separated elements
                elements = [elem.strip() for elem in inner.split(',')]
                return len(elements)
            else:
                # Single element (not a tuple)
                return 1
        elif isinstance(value, (list, tuple)):
            return len(value)
        else:
            # Single element
            return 1
    
    def _builtin_eq(self, val1, val2):
        """Equality comparison with type conversion"""
        # Helper function to convert string numbers to integers if possible
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():  # Handle negative numbers
                return int(val)
            return val
        
        # Convert both values if they are numeric strings
        converted_val1 = convert_if_number(val1)
        converted_val2 = convert_if_number(val2)
        
        # If one is int and the other is convertible, ensure both are int
        if isinstance(converted_val1, int) and not isinstance(converted_val2, int):
            converted_val2 = convert_if_number(val2)
        elif isinstance(converted_val2, int) and not isinstance(converted_val1, int):
            converted_val1 = convert_if_number(val1)
        
        print(f"Eq comparison: {val1} ({type(val1)}) vs {val2} ({type(val2)}) -> {converted_val1} vs {converted_val2}")
        
        return converted_val1 == converted_val2
    
    # Truth value operations
    def _builtin_or(self, val1, val2):
        """Logical OR operation"""
        def is_truthy(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.lower() in ['true', '1', 'yes'] or (val.isdigit() and int(val) != 0)
            if isinstance(val, (int, float)):
                return val != 0
            return bool(val)
        
        result = is_truthy(val1) or is_truthy(val2)
        print(f"OR operation: {val1} or {val2} = {result}")
        return result
    
    def _builtin_not(self, value):
        """Logical NOT operation"""
        def is_truthy(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.lower() in ['true', '1', 'yes'] or (val.isdigit() and int(val) != 0)
            if isinstance(val, (int, float)):
                return val != 0
            return bool(val)
        
        result = not is_truthy(value)
        print(f"NOT operation: not {value} = {result}")
        return result
    
    def _builtin_ne(self, val1, val2):
        """Not equal comparison"""
        result = not self._builtin_eq(val1, val2)
        print(f"NE comparison: {val1} != {val2} = {result}")
        return result
    
    # Integer operations
    def _builtin_power(self, val1, val2):
        """Power operation (**)"""
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            return val
        
        num1 = convert_if_number(val1)
        num2 = convert_if_number(val2)
        
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            result = num1 ** num2
            print(f"Power operation: {val1} ** {val2} = {result}")
            return result
        else:
            print(f"Power operation failed: {val1} ** {val2} (not numbers)")
            return f"Error: Cannot compute power of {val1} and {val2}"
    
    def _builtin_neg(self, value):
        """Negation operation - returns negative of a number"""
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            try:
                # Try to convert to float if it's a decimal
                return float(val)
            except (ValueError, TypeError):
                return val
        
        num = convert_if_number(value)
        
        if isinstance(num, (int, float)):
            result = -num
            print(f"Negation operation: neg({value}) = {result}")
            return result
        else:
            print(f"Negation operation failed: neg({value}) (not a number)")
            return f"Error: Cannot negate non-numeric value {value}"
    
    def _builtin_ls(self, val1, val2):
        """Less than operation (ls)"""
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            return val
        
        num1 = convert_if_number(val1)
        num2 = convert_if_number(val2)
        
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            result = num1 < num2
            return result
        else:
            # String comparison fallback
            result = str(val1) < str(val2)
            print(f"String less than operation: {val1} < {val2} = {result}")
            return result
    
    def _builtin_gr(self, val1, val2):
        """Greater than operation (gr)"""
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            return val
        
        num1 = convert_if_number(val1)
        num2 = convert_if_number(val2)
        
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            result = num1 > num2
            print(f"Greater than operation: {val1} > {val2} = {result}")
            return result
        else:
            # String comparison fallback
            result = str(val1) > str(val2)
            print(f"String greater than operation: {val1} > {val2} = {result}")
            return result
    
    def _builtin_le(self, val1, val2):
        """Less than or equal operation (le)"""
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            return val
        
        num1 = convert_if_number(val1)
        num2 = convert_if_number(val2)
        
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            result = num1 <= num2
            print(f"Less than or equal operation: {val1} <= {val2} = {result}")
            return result
        else:
            # String comparison fallback
            result = str(val1) <= str(val2)
            print(f"String less than or equal operation: {val1} <= {val2} = {result}")
            return result
    
    def _builtin_ge(self, val1, val2):
        """Greater than or equal operation (ge)"""
        def convert_if_number(val):
            if isinstance(val, str) and val.isdigit():
                return int(val)
            elif isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            return val
        
        num1 = convert_if_number(val1)
        num2 = convert_if_number(val2)
        
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            result = num1 >= num2
            print(f"Greater than or equal operation: {val1} >= {val2} = {result}")
            return result
        else:
            # String comparison fallback
            result = str(val1) >= str(val2)
            print(f"String greater than or equal operation: {val1} >= {val2} = {result}")
            return result
    
    # String operations
    def _builtin_stem(self, string_val):
        """Return the first character of a string (Stem S)"""
        if isinstance(string_val, str) and len(string_val) > 0:
            result = string_val[0]
            print(f"Stem operation: Stem({string_val}) = '{result}'")
            return result
        else:
            print(f"Stem operation failed: {string_val} is not a valid string")
            return ""
    
    def _builtin_stern(self, string_val):
        """Remove the first character from a string (Stern S)"""
        if isinstance(string_val, str) and len(string_val) > 0:
            result = string_val[1:]
            print(f"Stern operation: Stern({string_val}) = '{result}'")
            return result
        elif isinstance(string_val, str):
            print(f"Stern operation: Stern({string_val}) = '' (empty string)")
            return ""
        else:
            print(f"Stern operation failed: {string_val} is not a valid string")
            return ""
    
    def _builtin_conc(self, str1, str2):
        """Concatenate two strings (Conc S T)"""
        result = str(str1) + str(str2)
        print(f"Conc operation: Conc({str1}, {str2}) = '{result}'")
        return result
    
    def apply_unary_operator(self, operator, operand):
        """Apply unary operator to one operand"""
        try:
            # Handle built-in unary operations
            if operator in self.builtins:
                if operator == 'neg':
                    return self.builtins[operator](operand)
                elif operator == 'not':
                    return self.builtins[operator](operand)
            
            # Add other unary operators here if needed
            return f"Unknown unary operator: {operator}"
                
        except Exception as e:
            return f"Error applying unary {operator}: {e}"
    
    def apply_binary_operator(self, operator, left_operand, right_operand):
        """Apply binary operator to two operands"""
        try:
            # Convert string numbers to integers if possible
            def convert_if_number(val):
                if isinstance(val, str) and val.isdigit():
                    return int(val)
                elif isinstance(val, str) and val.lstrip('-').isdigit():
                    return int(val)
                return val
            
            left = convert_if_number(left_operand)
            right = convert_if_number(right_operand)
            
            # Handle built-in operations first
            if operator in self.builtins:
                if operator in ['or', 'eq', 'ne', 'ls', 'gr', 'le', 'ge', '**']:
                    return self.builtins[operator](left_operand, right_operand)
                elif operator == 'not':
                    # NOT is unary, but if used as binary, apply to left operand
                    return self.builtins[operator](left_operand)
            
            # Original binary operations
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                if right != 0:
                    return left / right
                else:
                    return "Division by zero error"
            elif operator == '<':
                return left < right
            elif operator == '>':
                return left > right
            elif operator == '=':
                return left == right
            elif operator == '&':
                return left and right
            elif operator == '|':
                return left or right
            elif operator == '.':
                # String concatenation or other dot operation
                return str(left) + str(right)
            elif operator == '@':
                # List/tuple concatenation or custom operation
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                return f"{left}@{right}"
            elif operator == ':':
                # Colon operation (could be list construction, etc.)
                return f"{left}:{right}"
            elif operator == '˜':
                # Tilde operation
                return f"{left}˜{right}"
            elif operator == '$':
                # Dollar operation
                return f"{left}${right}"
            elif operator == '!':
                # Factorial or negation-like operation
                return f"{left}!{right}"
            elif operator == '#':
                # Hash operation
                return f"{left}#{right}"
            elif operator == '%':
                # Modulo operation
                return left % right
            elif operator == 'ˆ':
                # Power operation
                return left ** right
            elif operator == '_':
                # Underscore operation
                return f"{left}_{right}"
            elif operator == '[':
                # Left bracket operation
                return f"{left}[{right}"
            elif operator == ']':
                # Right bracket operation
                return f"{left}]{right}"
            elif operator == '{':
                # Left brace operation
                return f"{left}{{{right}"
            elif operator == '}':
                # Right brace operation
                return f"{left}}}{right}"
            elif operator == '"':
                # Quote operation
                return f'{left}"{right}'
            elif operator == "'":
                # Single quote operation
                return f"{left}'{right}"
            elif operator == '?':
                # Question mark operation (ternary-like)
                return f"{left}?{right}"
            else:
                return f"Unknown operator: {operator}"
                
        except Exception as e:
            return f"Error applying {operator}: {e}"
    
    def parse_tuple(self, tuple_str):
        
        if not (tuple_str.startswith('(') and tuple_str.endswith(')')):
            return [tuple_str]
        
        # Remove outer parentheses
        content = tuple_str[1:-1].strip()
        if not content:
            return []
        
        elements = []
        current_element = ""
        bracket_count = 0
        brace_count = 0
        paren_count = 0
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(content):
            char = content[i]
            
            # Handle quotes
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    # Check if it's escaped
                    if i > 0 and content[i-1] != '\\':
                        in_quotes = False
                        quote_char = None
            
            # If we're inside quotes, just add the character
            if in_quotes:
                current_element += char
            else:
                # Track nested structures
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == ',' and bracket_count == 0 and brace_count == 0 and paren_count == 0:
                    # This is a top-level comma separator
                    elements.append(current_element.strip())
                    current_element = ""
                    i += 1
                    continue
                
                current_element += char
            
            i += 1
        
        # Add the last element
        if current_element.strip():
            elements.append(current_element.strip())
        
        return elements

    def convert_element_to_object(self, element_str):
        """
        Convert a string element to its proper object representation.
        Handles dictionaries, lists, and primitive values.
        """
        element_str = element_str.strip()
        
        # Handle dictionary objects
        if element_str.startswith('{') and element_str.endswith('}'):
            try:
                # Use eval to parse the dictionary (in a real implementation, use ast.literal_eval)
                return eval(element_str)
            except:
                return element_str
        
        # Handle list objects
        if element_str.startswith('[') and element_str.endswith(']'):
            try:
                return eval(element_str)
            except:
                return element_str
        
        # Handle nil
        if element_str == 'nil':
            return None
        
        # Handle numbers
        try:
            if '.' in element_str:
                return float(element_str)
            else:
                return int(element_str)
        except ValueError:
            pass
        
        # Return as string if nothing else matches
        return element_str
    
    def get_current_environment(self):
        """Get current environment from top of stack"""
        # Look for environment marker in stack (top-most e'c')
        for i in range(len(self.stack) - 1, -1, -1):
            item = self.stack[i]
            if isinstance(item, str) and item.startswith('e') and item != "eq":
                return item
        return "e0"  # Default to e0 if no environment found
    
    def create_new_environment(self, base_env, var_bindings):
        """Create new environment with variable bindings
        var_bindings can be a dict of {var_name: var_value} or single (var_name, var_value) tuple
        """
        self.env_counter += 1
        new_env_name = f"e{self.env_counter}"
        
        # Copy base environment
        if base_env in self.environments:
            self.environments[new_env_name] = self.environments[base_env].copy()
        else:
            self.environments[new_env_name] = {}
        
        # Add new variables
        if isinstance(var_bindings, dict):
            for var_name, var_value in var_bindings.items():
                self.environments[new_env_name][var_name] = var_value
        else:
            # Assume it's a (var_name, var_value) tuple for backward compatibility
            var_name, var_value = var_bindings
            self.environments[new_env_name][var_name] = var_value
        
        return new_env_name
    
    def lookup_variable(self, name, env_name):
        """Look up variable in specified environment"""
        if env_name in self.environments and name in self.environments[env_name]:
            return self.environments[env_name][name]
        elif name in self.builtins:
            return self.builtins[name]
        else:
            # Treat as literal if not found
            return name
    
    def apply_rator_rand(self, rator, rand):
        """Apply Rator to Rand"""
        if callable(rator):
            try:
                result = rator(rand)
                print(f"Applied {rator.__name__ if hasattr(rator, '__name__') else rator} to {rand} = {result}")
                return result
            except Exception as e:
                print(f"Error applying {rator} to {rand}: {e}")
                return f"Error applying {rator} to {rand}"
        else:
            print(f"Cannot apply {rator} to {rand} - not callable")
            return f"Cannot apply {rator} to {rand}"
    
    def step(self):
        """Execute one step of CSE machine"""
        if not self.control:
            return False
        
        # Pop rightmost element from control (CE)
        CE = self.control.pop()
        
        print(f"CE: {CE}")
        print(f"Control: {self.control}")
        print(f"Stack: {self.stack}")
        print("---")
        
        # NEW RULE: Unary Operators (like neg, not)
        if CE in self.unary_operators:
            if len(self.stack) >= 1:
                # Pop one element from stack
                operand = self.stack.pop()
                
                print(f"Unary operator {CE}: operand={operand}")
                
                # Apply unary operator
                result = self.apply_unary_operator(CE, operand)
                
                print(f"Unary operator result: {result}")
                
                # Push result back to stack
                self.stack.append(result)
            else:
                print(f"Unary operator {CE}: Not enough operands on stack")
                # Put the operator back or handle error - here we'll just push it as literal
                self.stack.append(CE)
        
        # NEW RULE: Binary Operators
        elif CE in self.binary_operators:
            if len(self.stack) >= 2:
                # Pop two elements from stack 
                left_operand = self.stack.pop()
                right_operand = self.stack.pop()
                
                print(f"Binary operator {CE}: left={left_operand}, right={right_operand}")
                
                # Apply binary operator
                result = self.apply_binary_operator(CE, left_operand, right_operand)
                
                print(f"Binary operator result: {result}")
                
                # Push result back to stack
                self.stack.append(result)
            else:
                print(f"Binary operator {CE}: Not enough operands on stack")
                # Put the operator back or handle error - here we'll just push it as literal
                self.stack.append(CE)
        
        # Rule for 'eq' builtin function
        elif CE == "eq":
            if len(self.stack) >= 2:
                # Pop two elements from stack for comparison
                right_operand = self.stack.pop()
                left_operand = self.stack.pop()
                
                print(f"Eq operation: left={left_operand}, right={right_operand}")
                
                # Apply equality comparison
                result = self._builtin_eq(left_operand, right_operand)
                
                print(f"Eq result: {result}")
                
                # Push result back to stack
                self.stack.append(result)
            else:
                print("Eq operation: Not enough operands on stack")
                self.stack.append(CE)
        
        
        
        # Rule 2: If CE is lambda'k'x' (single parameter) or lambda'k'x1,x2...xn (multiple parameters)
        elif isinstance(CE, str) and CE.startswith('lambda'):
            # Extract k and parameters from lambda'k'x' or lambda'k'x1,x2...xn
            lambda_part = CE[6:]  # Remove 'lambda'
            
            # Find the boundary between k and parameters
            k = ""
            params = ""
            for i, char in enumerate(lambda_part):
                if char.isalpha():
                    k = lambda_part[:i]
                    params = lambda_part[i:]
                    break
            
            # Parse parameters (split by comma if multiple)
            param_list = [p.strip() for p in params.split(',')]
            
            # Get current environment
            current_env = self.get_current_environment()
            
            # Create lambda object: lambda'c'k'x1,x2...xn'
            lambda_obj = {
                'type': 'lambda',
                'env': current_env,
                'k': k,
                'params': param_list  # Now stores list of parameters
            }
            self.stack.append(lambda_obj)
        
        # Rule 8: If CE is "beta"
        elif CE == "beta":
            if len(self.stack) >= 1 and len(self.control) >= 2:
                # Pop IsTrue from stack
                IsTrue = self.stack.pop()
                
                # Pop D1 and D2 from control
                D2 = self.control.pop()  # Rightmost first
                D1 = self.control.pop()
                
                print(f"Beta rule: IsTrue={IsTrue}, D1={D1}, D2={D2}")
                
                # Choose based on IsTrue value
                if IsTrue == True or IsTrue == "true" or (isinstance(IsTrue, str) and IsTrue.lower() == "true"):
                    # Use D1
                    if D1 in self.deltas:
                        # Push D1's delta contents to control
                        delta_contents = self.deltas[D1].copy()
                        self.control.extend(delta_contents)
                    else:
                        # If D1 is not a delta, push it directly
                        self.control.append(D1)
                else:
                    # Use D2
                    if D2 in self.deltas:
                        # Push D2's delta contents to control
                        delta_contents = self.deltas[D2].copy()
                        self.control.extend(delta_contents)
                    else:
                        # If D2 is not a delta, push it directly
                        self.control.append(D2)
            else:
                print("Beta rule: Not enough elements in stack or control")
        
        # Rule 9: FIXED TAU RULE - If CE starts with "tau" followed by a number
        elif isinstance(CE, str) and CE.startswith('tau'):
            # Extract the number after "tau"
            try:
                if len(CE) > 3:  # "tau" + number
                    num_elements = int(CE[3:])  # Extract number after "tau"
                else:
                    # If just "tau" with no number, pop all elements until environment marker
                    num_elements = None
                
                print(f"Tau rule: CE={CE}, num_elements={num_elements}")
                
                if num_elements is not None:
                    # Pop exactly num_elements from stack
                    elements_to_pop = []
                    for i in range(num_elements):
                        if self.stack:
                            element = self.stack.pop()
                            # Skip environment markers
                            if isinstance(element, str) and element.startswith('e') and element != "eq":
                                # Put environment marker back and don't count it
                                self.stack.append(element)
                                continue
                            elements_to_pop.append(element)
                        else:
                            break  # Not enough elements on stack
                    
                    # Reverse to get original order (since we popped from top)
                    elements_to_pop = elements_to_pop[::-1]
                else:
                    # Original behavior for just "tau" - pop until environment marker
                    elements_to_pop = []
                    temp_stack = []
                    while self.stack:
                        element = self.stack.pop()
                        if isinstance(element, str) and element.startswith('e') and element != "eq":
                            # Hit environment marker, put it back
                            self.stack.append(element)
                            break
                        temp_stack.append(element)
                    
                    # Reverse to get original order
                    elements_to_pop = temp_stack[::-1]
                
                # Create tuple representation
                if elements_to_pop:
                    tuple_repr = f"({', '.join(str(x) for x in elements_to_pop)})"
                else:
                    tuple_repr = "()"
                
                print(f"Tau rule: Created tuple {tuple_repr} from elements {elements_to_pop}")
                
                # Push tuple back to stack
                self.stack.append(tuple_repr)
                
            except ValueError:
                # If we can't parse the number, treat as literal
                print(f"Tau rule: Could not parse number from {CE}, treating as literal")
                self.stack.append(CE)
        
        # Rule 3, 4, 6, 7, NEW: If CE is "gamma"
        elif CE == "gamma":
            if len(self.stack) >= 1:
                top_element = self.stack.pop()
                print(f"Gamma: popped top element: {top_element} (type: {type(top_element)})")
                
                # Convert string representations back to objects if needed
                if isinstance(top_element, str):
                    # Check if it's a neeta object string
                    if top_element.startswith("{'type': 'neeta'") and top_element.endswith('}'):
                        try:
                            top_element = eval(top_element)  # Convert string to dict
                            print(f"Converted neeta string to object: {top_element}")
                        except:
                            pass  # Keep as string if conversion fails
                    # Check if it's a lambda object string
                    elif top_element.startswith("{'type': 'lambda'") and top_element.endswith('}'):
                        try:
                            top_element = eval(top_element)  # Convert string to dict
                            print(f"Converted lambda string to object: {top_element}")
                        except:
                            pass  # Keep as string if conversion fails
                
                # NEW RULE: If top element is a tuple, pop index I and push back I-th element
                if isinstance(top_element, str) and top_element.startswith('(') and top_element.endswith(')'):
                    if len(self.stack) >= 1:
                        index_element = self.stack.pop()
                        print(f"Gamma tuple indexing: tuple={top_element}, index={index_element}")
                        
                        # Parse the tuple to get elements
                        tuple_elements = self.parse_tuple(top_element)
                        
                        # REVERSE the tuple before indexing
                        reversed_tuple = tuple_elements[::-1]
                        print(f"Original tuple elements: {tuple_elements}")
                        print(f"Reversed tuple elements: {reversed_tuple}")
                        
                        # Convert index to integer if it's a string
                        try:
                            if isinstance(index_element, str):
                                index = int(index_element)
                            else:
                                index = index_element
                            
                            # Check if index is valid (1-based indexing on reversed tuple)
                            if 1 <= index <= len(reversed_tuple):
                                selected_element = reversed_tuple[index - 1]  # Convert to 0-based
                                print(f"Selected element {index} from reversed tuple: {selected_element}")
                                self.stack.append(selected_element)
                            else:
                                print(f"Index {index} out of bounds for tuple with {len(reversed_tuple)} elements")
                                self.stack.append(None)  # Push nil for out of bounds
                        except (ValueError, TypeError):
                            print(f"Invalid index: {index_element}")
                            self.stack.append(None)  # Push nil for invalid index
                    else:
                        # Put tuple back if no index available
                        print("Gamma tuple indexing: no index element available")
                        self.stack.append(top_element)
                
                # Rule 6: If top element is "Y"
                elif top_element == "Y":
                    if len(self.stack) >= 1:
                        lambda_element = self.stack.pop()
                        if isinstance(lambda_element, dict) and lambda_element.get('type') == 'lambda':
                            # Create neeta object with c, x, k
                            neeta_obj = {
                                'type': 'neeta',
                                'env': lambda_element['env'],  # c
                                'params': lambda_element['params'],  # x (now list)
                                'k': lambda_element['k']  # k
                            }
                            self.stack.append(neeta_obj)
                        else:
                            # Put back if not lambda
                            self.stack.append(lambda_element)
                            self.stack.append(top_element)
                    else:
                        # Put back if no second element
                        self.stack.append(top_element)
                
                # Rule 7: If top element is neeta
                elif isinstance(top_element, dict) and top_element.get('type') == 'neeta':
                    # Push lambda with c, x, k
                    lambda_obj = {
                        'type': 'lambda',
                        'env': top_element['env'],  # c
                        'params': top_element['params'],  # x (now list)
                        'k': top_element['k']  # k
                    }
                    # Push neeta back
                    self.stack.append(top_element)
                    self.stack.append(lambda_obj)
                    
                    self.control.append("gamma")
                    self.control.append("gamma")
                
                # Rule 4 (Enhanced): If top element is lambda
                elif isinstance(top_element, dict) and top_element.get('type') == 'lambda':
                    if len(self.stack) >= 1:
                        rand = self.stack.pop()
                        print(f"Gamma: applying lambda to {rand}")
                        
                        base_env = top_element['env']
                        param_list = top_element['params']
                        
                        # NEW RULE: Multi-parameter lambda with tuple destructuring
                        if len(param_list) > 1:
                            # Multi-parameter lambda - expect tuple
                            tuple_elements = self.parse_tuple(rand)
                            print(f"Multi-param lambda: params={param_list}, tuple_elements={tuple_elements}")
                            
                            # Create variable bindings: T=second element, N=first element (swapped)
                            var_bindings = {}
                            # For lambda5T,N with tuple (5, (5,4,3,2,1)): T should get (5,4,3,2,1), N should get 5
                            if len(param_list) == 2 and len(tuple_elements) >= 2:
                                var_bindings[param_list[0]] = tuple_elements[1]  # T gets second element
                                var_bindings[param_list[1]] = tuple_elements[0]  # N gets first element
                                print(f"Binding {param_list[0]} = {var_bindings[param_list[0]]}")
                                print(f"Binding {param_list[1]} = {var_bindings[param_list[1]]}")
                            else:
                                # Fallback to original order for other cases
                                for i, param_name in enumerate(param_list):
                                    if i < len(tuple_elements):
                                        var_bindings[param_name] = tuple_elements[len(tuple_elements)-1-i]
                                    else:
                                        # If not enough tuple elements, bind to nil/None
                                        var_bindings[param_name] = None
                                    print(f"Binding {param_name} = {var_bindings[param_name]}")
                            
                            # Create new environment with all bindings
                            new_env = self.create_new_environment(base_env, var_bindings)
                        else:
                            # Single parameter lambda - original behavior
                            param_name = param_list[0]
                            new_env = self.create_new_environment(base_env, (param_name, rand))
                        
                        # Push new environment onto stack
                        self.stack.append(new_env)
                        
                        # Push new environment and corresponding delta onto control
                        delta_name = f"delta{top_element['k']}"
                        self.control.append(new_env)
                        self.control.append(delta_name)
                    else:
                        # Put back if no second element
                        self.stack.append(top_element)
                
                # Rule 3: Regular function application
                else:
                    if len(self.stack) >= 1:
                        rand = self.stack.pop()
                        print(f"Gamma: applying {top_element} to {rand}")
                        result = self.apply_rator_rand(top_element, rand)
                        self.stack.append(result)
                    else:
                        # Put back if no second element
                        print(f"Gamma: not enough elements, putting back {top_element}")
                        self.stack.append(top_element)
        
        # Handle delta expansion
        elif isinstance(CE, str) and CE.startswith('delta'):
            if CE in self.deltas:
                # Replace delta with its contents in control
                # Add delta contents in correct order (rightmost first since we pop from right)
                delta_contents = self.deltas[CE].copy()
                # Extend control with delta contents in original order
                self.control.extend(delta_contents)
            else:
                print(f"Unknown delta: {CE}")
        
        # Rule 5: If CE is ek (environment marker)
        elif isinstance(CE, str) and CE.startswith('e') and CE != "eq":
            if len(self.stack) >= 1:
                popped_elements = []
                found_matching_marker = False
                
                # Pop elements until we find the matching environment marker
                while self.stack:
                    popped_element = self.stack.pop()
                    if popped_element == CE:
                        found_matching_marker = True
                        break
                    popped_elements.append(popped_element)
                
                if found_matching_marker:
                    # Remove the matching environment marker from control stack
                    if CE in self.control:
                        self.control.remove(CE)
                    
                    # Push back all popped elements (except the matching marker) in reverse order
                    for element in reversed(popped_elements):
                        self.stack.append(element)
                else:
                    # If matching marker not found, push back all popped elements
                    for element in reversed(popped_elements):
                        self.stack.append(element)
                    # And push the CE marker as well since it wasn't found
                    self.stack.append(CE)
            else:
                # If stack is empty, just push environment marker
                self.stack.append(CE)

        # Rule 1: If CE is a variable name
        elif isinstance(CE, str) and not CE.startswith(('lambda', 'delta', 'gamma', 'beta', 'tau', 'aug', 'e')):
            current_env = self.get_current_environment()
            value = self.lookup_variable(CE, current_env)
            self.stack.append(value)
        
        # Handle literals
        else:
            self.stack.append(CE)
        
        return True
    
    def run(self):
        """Run CSE machine until control is empty"""
        step_count = 0
        while step_count<10000 :  # Safety limit
            if not self.step():
                break
            step_count += 1
        
        print(f"\nFinal state after {step_count} steps:")
        print(f"Stack: {self.stack}")
        print(f"Control: {self.control}")
        return self.stack[-1] if self.stack else None

# Initialize and run the machine
# if __name__ == "__main__":
#     machine = CSEMachine()
    
#     # Initial state: Stack has e0, Control has e0, delta0
#     machine.stack = ["e0"]
#     machine.control = ["e0", "delta0"]
    
#     print("Initial state:")
#     print(f"Stack: {machine.stack}")
#     print(f"Control: {machine.control}")
#     print(f"Environment e0: {machine.environments['e0']}")
#     print("\nStarting execution:\n")
    
#     result = machine.run()
#     print(f"\nFinal result: {result}")
