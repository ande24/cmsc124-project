import re

# Define token types with regex patterns
TOKEN_SPECIFICATION = [
    ('DATA_TYPE',       r'\b(?:int|char|string|float)\b'), # Data type
    ('INPUT',           r'(?:cin >>)|(?:cin>>)'),
    ('OUTPUT',          r'cout'),
    ('OUTPUT_CASE',     r'<<'),
    ('NUMBER',          r'\d+(\.\d*)?'),  # Integer or decimal number
    ('STRING',          r'(?:"[^"]*")|(?:\'[^\']*\')'),
    ('VARIABLE_NAME',   r'[A-Za-z_]\w*'),  # Identifiers (variable names)
    ('OPERATOR',        r'[+\-*/=]'),     # Arithmetic operators
    ('PUNCTUATION',     r'[,\(\)]'),       # Punctuation
    ('IF_STATEMENT',    r'\b(?:if)\b'),
    ('FOR_STATEMENT',   r'\b(?:for)\b'),
    ('SEMI_COLON',      r';'),
    ('START_IF_FOR',    r'{'), 
    ('END_IF_FOR',      r'}'), 
    ('SKIP',            r'[ \t]+'),       # Spaces and tabs (to skip)
    ('NEWLINE',         r'\n'),           # Line breaks
    ('MISMATCH',        r'.'),            # Any other character
]

# Token class for structured storage
class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, Line {self.line}, Col {self.column})"

def lexical_analyzer(text):
    tokens = []
    line_num = 1
    line_start = 0
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    for match in re.finditer(token_regex, text):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start
        # print("MATCH:", match, "match start:", match.start(), "line start", line_start)
        if kind == 'NEWLINE':
            line_num += 1
            line_start = match.end()
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character {value} on line {line_num}, column {column}")
        else:
            tokens.append(Token(kind, value, line_num, column))
            # print("tokens:", tokens)
    return tokens

# Example usage
if __name__ == "__main__":
    input_code = """
    int x = 4;
    int y = x + 2 * (3 - 1);
    cout << y;
    """
    tokens = lexical_analyzer(input_code)
    for token in tokens:
        print(token)
