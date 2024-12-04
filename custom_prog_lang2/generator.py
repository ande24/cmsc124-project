import lexer
import parser

class Generator:
    def __init__(self):
        self.mips_code = []
        self.data_segment = [".data"]
        self.text_segment = [".text", ".globl main", "main:"]
        self.temp_register_counter = 0

    def generate_mips(self, ast):
        """
        Generate MIPS code from the AST.
        """
        for node in ast:
            if node['type'] == 'variable_declaration':
                self.handle_variable_declaration(node)
            elif node['type'] == 'variable_assignment':
                self.handle_variable_assignment(node)
            elif node['type'] == 'input_statement':
                self.handle_input_statement(node)
            elif node['type'] == 'output_statement':
                self.handle_output_statement(node)
            elif node['type'] == 'comment':
                self.handle_comment(node)
            elif node['type'] == 'if_statement':
                self.handle_if_statement(node)

        return self.generate_output()

    def get_temp_register(self):
        reg = f"$t{self.temp_register_counter}"
        self.temp_register_counter = (self.temp_register_counter + 1) % 10
        return reg

    def handle_variable_declaration(self, node):
        if node.get('value') is None:
            self.data_segment.append(f"{node['variable']}: .word 0")
        else:
            # if node['expression']['type'] == 'binary_operation':

            # else:
            self.data_segment.append(f"{node['variable']}: .word {node['value']}")

    def handle_variable_assignment(self, node):
        variable = node['variable']
        expression = node['expression']
        temp_reg = self.get_temp_register()

        if expression['type'] == 'number':
            self.text_segment.append(f"li {temp_reg} {expression['value']}")
        elif expression['type'] == 'variable':
            self.text_segment.append(f"lw {temp_reg}, {expression['name']}")
        elif expression['type'] == 'binary_operation':
            self.handle_binary_operation(expression, {temp_reg})
        
        self.text_segment.append(f"sw {temp_reg}, {variable}")

    def handle_binary_operation(self, node, target_register):
        left = node['left']
        right = node['right']
        operator = node['operator']
        allocate_reg_left = self.get_temp_register()
        allocate_reg_right = self.get_temp_register()

        # Load left operand
        if left['type'] == 'number':
            self.text_segment.append(f"li {allocate_reg_left}, {left['value']}")
        elif left['type'] == 'variable':
            self.text_segment.append(f"lw {allocate_reg_left}, {left['name']}")

        # Load right operand
        if right['type'] == 'number':
            self.text_segment.append(f"li {allocate_reg_right}, {right['value']}")
        elif right['type'] == 'variable':
            self.text_segment.append(f"lw {allocate_reg_right}, {right['name']}")

        # Perform operation
        if operator == '+':
            self.text_segment.append(f"add {list(target_register)[0]}, {allocate_reg_left}, {allocate_reg_right}")
        elif operator == '-':
            self.text_segment.append(f"sub {list(target_register)[0]}, {allocate_reg_left}, {allocate_reg_right}")
        elif operator == '*':
            self.text_segment.append(f"mul {list(target_register)[0]}, {allocate_reg_left}, {allocate_reg_right}")
        elif operator == '/':
            self.text_segment.append(f"div {list(target_register)[0]}, {allocate_reg_left}, {allocate_reg_right}")
            self.text_segment.append(f"mflo {list(target_register)[0]}")

    def handle_input_statement(self ,node):
        variable = node['variable']
        self.text_segment.append(f"li $v0, 5")  # Read integer
        self.text_segment.append(f"syscall")
        self.text_segment.append(f"sw $v0, {variable}")

    def handle_output_statement(self, node):
        for expr in node['expressions']:
            if expr['type'] == 'string':
                label = f"str_{len(self.data_segment)}"
                self.data_segment.append(f"{label}: .asciiz {expr['value']}")
                self.text_segment.append(f"la $a0, {label}")
                self.text_segment.append(f"li $v0, 4")  # Print string
            elif expr['type'] == 'variable':
                self.text_segment.append(f"lw $a0, {expr['name']}")
                self.text_segment.append(f"li $v0, 1")  # Print integer
            self.text_segment.append(f"syscall")

    # def handle_comment(self, node):


    # def handle_if_statement(self, node):

    
    def generate_output(self):
        self.mips_code.extend(self.data_segment)

        self.mips_code.extend(self.text_segment)
        self.mips_code.extend([
        "li $v0, 10",
        "syscall"
        ])
        return "\n".join(self.mips_code)

def main():
    input_code = """
    int x;
    cout << "Give me a number: ";
    cin >> x;
    int y;
    y = x + 4;
    cout << y;
    """

    tokens = lexer.lexical_analyzer(input_code)
    parse_to_mips = parser.Parser(tokens)
    ast = parse_to_mips.parse()

    generator = Generator()
    mips_code = generator.generate_mips(ast)

    # output_file = "output.asm"
    # with open(output_file, "w") as file:
    #     file.write(mips_code)

    print(mips_code)

if __name__ == "__main__":
    main()
