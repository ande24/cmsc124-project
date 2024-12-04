import re

# Define token types with regex patterns
TOKEN_SPECIFICATION = [
    ('DATA_TYPE',       r'\b(?:tally|rune|verse|portion)\b'), # Data type
    ('INPUT',           r'(?:summon)'),
    ('OUTPUT',          r'cast'),
    ('OUTPUT_CASE',     r'spell'),
    ('NUMBER',          r'\d+(\.\d*)?'),  # Integer or decimal number
    ('CHAR',            r'(?:"[^"]")|(?:\'[^\']\')'),
    ('STRING',          r'(?:"[^"]*")|(?:\'[^\']*\')'),
    ('OPERATOR',        r'(imbue with|augmented by|diminished by|amplified by|fragmented by|augment by|diminish by|amplify by|fragment by|and|or|is inferior to|is superior to|is inferior or equal to|is superior or equal to|is equal to|is unequal to)'), 
    ('PUNCTUATION',     r'[,\(\)]'),       # Punctuation
    ('IF_STATEMENT',    r'\b(?:trial)\b'),
    ('ELSE_STATEMENT',  r'\b(?:failure)\b'),
    ('FOR_STATEMENT',   r'\b(?:cycle)\b'),
    ('VARIABLE_NAME',   r'[A-Za-z_]\w*'),  # Identifiers (variable names)
    ('SEMI_COLON',      r';'),
    ('START_IF_FOR',    r'{'), 
    ('END_IF_FOR',      r'}'), 
    ('SKIP',            r'[ \t]+'),       # Spaces and tabs (to skip)
    ('NEWLINE',         r'\n'),           # Line breaks
    ('SINGLE_COMMENT',  r'//[^\n]*'),  # Single-line comment (//)
    ('MULTI_COMMENT', r'/\*.*?\*/'),  # Multi-line comment (/*...*/)
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
    
    complete_regex = re.compile(token_regex, re.DOTALL)

    for match in re.finditer(complete_regex, text):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start
        # print("MATCH:", match, "match start:", match.start(), "line start", line_start)
        if kind == 'NEWLINE':
            line_num += 1
            line_start = match.end()
        elif kind == 'SKIP' or kind in ['SINGLE_COMMENT', 'MULTI_COMMENT']:
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
    tally x = 4;
    tally y = x + 2 * (3 - 1);
    verse f = 1.1;
    portion s = "sdfe"
    rune c = 's';
    cout << y;
    """
    
    tokens = lexical_analyzer(input_code)
    for token in tokens:
        print(token)

