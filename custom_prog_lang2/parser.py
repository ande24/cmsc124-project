import lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.symbol_table = {}
    
    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def consume(self, expected_type=None):
        if self.current >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        
        token = self.tokens[self.current]
        
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.type}")
        
        self.current += 1
        return token
    
    def parse(self):
        """
        Top-level parsing method
        This implements a simple grammar for variable declarations and assignments
        """
        statements = []
        while self.peek():
            statements.append(self.parse_statement())
        return statements
    
    def parse_statement(self):
        """Parse a single statement (currently supports variable declaration and assignment)"""
        token = self.peek()

        print(token, token.type)
        
        if token.type == 'DATA_TYPE':
            return self.parse_variable_declaration()
        elif token.type == 'INPUT':
            return self.parse_input_statement()
        elif token.type == 'OUTPUT':
            return self.parse_output_statement()
        elif token.type == 'IF_STATEMENT':
            return self.parse_if_statement()
        elif token.type == 'VARIABLE_NAME':
            return self.parse_variable_statement()
        else:
            raise SyntaxError(f"Unexpected token: {token}")
        
    def parse_input_statement(self):
        """
        Parse `cin >> variable;` and update the variable's value in the symbol table.
        """
        self.consume('INPUT') 
        var_name = self.consume('VARIABLE_NAME') 

        if var_name.value not in self.symbol_table:
            raise SyntaxError(f"Variable '{var_name.value}' not declared")

        data_type = self.symbol_table[var_name.value]['data_type']
        user_input = input(f"Enter value for {var_name.value}: ")

        try:
            if data_type == 'tally':
                self.symbol_table[var_name.value]['value'] = int(user_input)
            elif data_type == 'portion':
                self.symbol_table[var_name.value]['value'] = float(user_input)
            elif data_type == 'verse':  # Assuming you support a 'string' type
                self.symbol_table[var_name.value]['value'] = user_input
            else:
                raise TypeError(f"Unsupported data type: {data_type}")
        except ValueError:
            raise SyntaxError(f"Invalid input for variable '{var_name.value}' of type '{data_type}'")

        # Consume the semicolon
        self.consume('SEMI_COLON')

        # Return the parsed input statement
        return {
            'type': 'input_statement',
            'variable': var_name.value,
            'value': self.symbol_table[var_name.value]['value']
        }

    def parse_output_statement(self):
        """
        Parse `cout << expression;`
        """
        self.consume('OUTPUT')  # Consume `cout`
        self.consume('OUTPUT_CASE')  # Consume the initial `<<`
        expressions = []

        # Parse one or more expressions separated by `<<`
        while True:
            current_token = self.peek()

            if current_token.type == 'STRING':  # Handle string literals
                string_token = self.consume('STRING')
                expressions.append({
                    'type': 'string',
                    'value': string_token.value
                })
            elif current_token.type == 'VARIABLE_NAME':  # Handle variable names
                var_name = self.consume('VARIABLE_NAME').value
                if var_name not in self.symbol_table:
                    raise SyntaxError(f"Variable '{var_name}' not declared")
                expressions.append({
                    'type': 'variable',
                    'name': var_name,
                    'value': self.symbol_table[var_name]['value']
                })
            else:
                raise SyntaxError(f"Unexpected token in output statement: {current_token}")

            # Check for another `<<`
            if self.peek() and self.peek().type == 'OUTPUT_CASE':
                self.consume('OUTPUT_CASE')  # Consume `<<` to continue parsing
            else:
                break  # No more expressions to process

        self.consume('SEMI_COLON')  # Consume the semicolon at the end of the statement

        # Return the parsed output statement as an AST node
        return {
            'type': 'output_statement',
            'expressions': expressions
        }

    def parse_variable_declaration(self):
        """
        Parse variable declaration of the form:
        data_type variable_name = expression;
        """
        # Consume data type
        data_type = self.consume('DATA_TYPE')
        
        # Variable name
        var_name = self.consume('VARIABLE_NAME')
        
        if var_name.value in self.symbol_table:
            raise SyntaxError(f"Variable {var_name.value} already declared")
        self.symbol_table[var_name.value] = {'data_type': data_type.value, 'value': None} 

        current_token = self.peek()

        if current_token.type == 'SEMI_COLON':
            self.consume('SEMI_COLON')
            return {
                'type': 'variable_declaration',
                'data_type': data_type.value,
                'variable': var_name.value,
            }

        # Assignment operator
        self.consume('OPERATOR')
        
        # Parse expression
        expression = self.parse_expression()
        value = self.evaluate_expression(expression) 

        if data_type.value == 'rune':
            if not isinstance(value, str) or len(value) != 1:
                # raise SyntaxError(f"Expected a single character for '{var_name.value}', got {value}")
                print("DATA TYPEEEE:", data_type, "LENGTHH:", len(value))
        
        # Semicolon
        self.consume('SEMI_COLON')

        self.symbol_table[var_name.value]['value'] = value
        
        return {
            'type': 'variable_declaration',
            'data_type': data_type.value,
            'variable': var_name.value,
            'value': value,
            'expression': expression
        }
    
    def parse_variable_statement(self):
        """
        Parse a variable statement, which includes assignments:
        variable_name = expression;
        """
        # Consume the variable name
        var_name = self.consume('VARIABLE_NAME').value
        
        # Check if the variable is declared
        if var_name not in self.symbol_table:
            raise SyntaxError(f"Variable '{var_name}' not declared")
        
        # Consume the assignment operator
        self.consume('OPERATOR') 
        
        # Parse the expression after '='
        expression = self.parse_expression()
        
        # Evaluate the expression to get the assigned value
        value = self.evaluate_expression(expression)
        
        # Update the symbol table with the new value
        self.symbol_table[var_name]['value'] = value
        
        # Consume the semicolon
        self.consume('SEMI_COLON')
        
        # Return the parsed assignment statement as an AST node
        return {
            'type': 'variable_assignment',
            'variable': var_name,
            'value': value,
            'expression': expression
        }
    
    def parse_expression(self):
        """
        Parse arithmetic expressions with basic precedence
        Supports: 
        - Numbers 
        - Variables
        - Parenthesized expressions
        - Basic arithmetic operations (+, -, *, /)
        - Compound assignment operations (+=, -=, *=, /=)
        """
        return self.parse_additive_expression()
    
    def parse_additive_expression(self):
        """
        Handle addition and subtraction
        Supports expressions like: x augmented by y, z diminished by w, etc. as well as the compound assignment versions
        """
        left = self.parse_multiplicative_expression()
        
        while self.peek() and self.peek().type == 'OPERATOR' and self.peek().value in ['augmented by', 'diminished by', 'augment by', 'diminish by']:
            value = self.peek().value
            operator = self.consume('OPERATOR')
            right = self.parse_multiplicative_expression()
            if value in ['augmented by', 'diminished by']:
                left = {
                    'type': 'binary_operation',
                    'operator': operator.value,
                    'left': left,
                    'right': right
                }
            else:
                left = {
                    'type': 'compound_assignment',
                    'operator': operator.value,
                    'left': left,
                    'right': right
                }
        return left
    
    def parse_multiplicative_expression(self):
        """
        Handle multiplication and division
        Supports expressions like: x * y, z / w, etc. as well as the compound assignment versions
        """
        left = self.parse_primary_expression()
        
        while self.peek() and self.peek().type == 'OPERATOR'and self.peek().value in ['amplified by', 'fragmented by', 'amplify by', 'fragment by']:
            value = self.peek().value
            operator = self.consume('OPERATOR')
            right = self.parse_primary_expression()
            if value in ['amplified by', 'fragmented by']:
                left = {
                    'type': 'binary_operation',
                    'operator': operator.value,
                    'left': left,
                    'right': right
                }
            else:
                left = {
                    'type': 'compound_assignment',
                    'operator': operator.value,
                    'left': left,
                    'right': right
                }
        
        return left
    
    def parse_if_statement(self):
        """Parse an if statement of the form:
        trial (condition) { statements }
        Optionally followed by a failure block:
        failure { statements }
        """
        self.consume('IF_STATEMENT')  # Consume 'trial' (if)

        # Consume opening parenthesis
        self.consume('PUNCTUATION')

        # Parse the condition expression (inside parentheses)
        condition = self.parse_condition_expression()

        # Consume closing parenthesis
        self.consume('PUNCTUATION')

        # Parse the 'if' block (statements inside { })
        if_block = self.parse_block()

        # Check if there's a failure block
        failure_block = None
        if self.peek() and self.peek().type == 'ELSE_STATEMENT':
            self.consume('ELSE_STATEMENT')  # Consume 'failure'
            failure_block = self.parse_block()  # Parse the failure block

        return {
            'type': 'if_statement',
            'condition': condition,
            'if_block': if_block,
            'failure_block': failure_block
        }
    
    def parse_block(self):
        """Parse a block of statements enclosed in braces {}"""
        self.consume('START_IF_FOR')  # Consume '{'

        statements = []
        while self.peek() and self.peek().type != 'END_IF_FOR':
            statements.append(self.parse_statement())

        self.consume('END_IF_FOR')  # Consume '}'
        return statements
    
    def parse_condition_expression(self):
        return self.parse_logical_expression()
    
    def parse_logical_expression(self):
        """Handle logical AND and OR (&&, ||)"""
        left = self.parse_relational_expression()

        while self.peek() and self.peek().type == 'OPERATOR' and self.peek().value in ['and', 'or']:
            operator = self.consume('OPERATOR')
            right = self.parse_relational_expression()
            left = {
                'type': 'logical_operation',
                'operator': operator.value,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_relational_expression(self):
        """Handle relational operations like <, >, <=, >=, ==, !="""
        left = self.parse_additive_expression()

        while self.peek() and self.peek().type == 'OPERATOR' and self.peek().value in ['is inferior to', 'is superior to', 'is inferior or equal to', 'is superior or equal to', 'is equal to', 'is unequal to']:
            operator = self.consume('OPERATOR')
            right = self.parse_additive_expression()
            left = {
                'type': 'binary_operation',
                'operator': operator.value,
                'left': left,
                'right': right
            }

        return left
    
    def parse_primary_expression(self):
        """
        Parse primary expressions:
        - Numbers
        - Variables
        - Characters
        - Strings
        - Parenthesized expressions
        """
        token = self.peek()
        
        if token.type == 'NUMBER':
            if '.' in token.value:
                return {
                    'type': 'number',
                    'value': float(self.consume('NUMBER').value)
                }
            return {
                'type': 'number',
                'value': int(self.consume('NUMBER').value)
            }
        elif token.type == 'VARIABLE_NAME':
            var_name = self.consume('VARIABLE_NAME').value
            if var_name not in self.symbol_table:
                raise SyntaxError(f"Variable '{var_name}' not declared") 
            return {
                'type': 'variable',
                'name': var_name,
                'value': self.symbol_table[var_name]['value']
            }
        elif token.type == 'CHAR':  # Handle characters
            return {
                'type': 'char',
                'value': self.consume('CHAR').value.strip("'")
            }
        elif token.type == 'STRING':  # Handle string literals
            return {
                'type': 'string',
                'value': self.consume('STRING').value
            }
        elif token.type == 'PUNCTUATION' and token.value == '(':
            self.consume('PUNCTUATION')  # consume '('
            expr = self.parse_expression()      
            self.consume('PUNCTUATION')  # consume ')'
            return expr
        
        raise SyntaxError(f"Unexpected token in expression: {token}")
    
    def evaluate_expression(self, node):
        """
        Evaluate the parsed expression tree.
        """
        if node['type'] == 'number':
            return node['value']
        elif node['type'] == 'variable':
            return node['value']
        elif node['type'] == 'char':
            return node['value']
        elif node['type'] == 'string':
            return node['value']
        elif node['type'] == 'binary_operation':
            left_val = self.evaluate_expression(node['left'])
            right_val = self.evaluate_expression(node['right'])
            operator = node['operator']
            if operator == 'augmented by':
                return left_val + right_val
            elif operator == 'diminished by':
                return left_val - right_val
            elif operator == 'amplified by':
                return left_val * right_val
            elif operator == 'fragmented by':
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_val / right_val
        raise ValueError(f"Unknown node type: {node['type']}") 

    def get_symbol_table(self):
        return self.symbol_table
    
def main():
    input_code = """
    tally a imbue with 5;
    tally b imbue with 6;
    trial (a is inferior to b) {
        cast spell "victory";
    }
    failure {
        cast spell "defeat";
    }
    """
    
    # Tokenize
    tokens = lexer.lexical_analyzer(input_code)
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Print Abstract Syntax Tree (AST)
    import json
    print(json.dumps(ast, indent=2))

    # Print Symbol Table
    # print("\nSymbol Table:")
    # print(json.dumps(parser.symbol_table, indent=2)) 

if __name__ == "__main__":
    main()