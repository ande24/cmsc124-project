import lexer
import parser

class Generator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.mips_code = []
        self.data_segment = [".data"]
        self.text_segment = [".text", ".globl main", "main:"]
        self.temp_register_counter = 0
        self.buffer = 0

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
    
    def get_buffer(self, variable):
        return f"{variable}_buffer"

    def handle_variable_declaration(self, node):
        variable = node['variable']
        if node.get('value') is None:
            if self.symbol_table[variable]['data_type'] == "tally":
                self.data_segment.append(f"{variable}: .word 0")
            # elif self.symbol_table[variable]['data_type'] == "verse":
            #     buffer_label = self.get_buffer(variable)
                # if f"{buffer_label}: .space" not in self.data_segment:
                #     self.data_segment.append(f"{buffer_label}: .space 100")
        else:
            if self.symbol_table[variable]['data_type'] == "tally":
                self.data_segment.append(f"{variable}: .word {node['value']}")
            elif self.symbol_table[variable]['data_type'] == "verse":
                buffer_label = self.get_buffer(variable)
                if f"{buffer_label}: .space" not in self.data_segment:
                    self.data_segment.append(f"{buffer_label}: .space 100")

    def handle_variable_assignment(self, node):
        variable = node['variable']
        expression = node['expression']
        var_info = self.symbol_table[variable]

        if var_info['data_type'] == "verse":
            buffer_label = self.get_buffer(variable)
            if expression['type'] == 'string':
                # Store string directly in the buffer
                temp_label = f"str_{len(self.data_segment)}"
                self.data_segment.append(f"{temp_label}: .asciiz {expression['value']}")
                self.text_segment.append(f"la $t0, {temp_label}")
                self.text_segment.append(f"la $t1, {buffer_label}")
                self.text_segment.append(f"li $t2, 100")  # Assuming a max size of 100 bytes
                self.text_segment.append(f"loop_copy:")
                self.text_segment.append(f"lb $t3, 0($t0)")
                self.text_segment.append(f"sb $t3, 0($t1)")
                self.text_segment.append(f"beqz $t3, end_copy")
                self.text_segment.append(f"addi $t0, $t0, 1")
                self.text_segment.append(f"addi $t1, $t1, 1")
                self.text_segment.append(f"subi $t2, $t2, 1")
                self.text_segment.append(f"bnez $t2, loop_copy")
                self.text_segment.append(f"end_copy:")
            elif expression['type'] == 'variable':
                # Copy from one string buffer to another
                source_buffer = self.get_buffer(expression['name'])
                self.text_segment.append(f"la $t0, {source_buffer}")
                self.text_segment.append(f"la $t1, {buffer_label}")
                self.text_segment.append(f"li $t2, 100")  # Assuming a max size of 100 bytes
                self.text_segment.append(f"loop_copy_var:")
                self.text_segment.append(f"lb $t3, 0($t0)")
                self.text_segment.append(f"sb $t3, 0($t1)")
                self.text_segment.append(f"beqz $t3, end_copy_var")
                self.text_segment.append(f"addi $t0, $t0, 1")
                self.text_segment.append(f"addi $t1, $t1, 1")
                self.text_segment.append(f"subi $t2, $t2, 1")
                self.text_segment.append(f"bnez $t2, loop_copy_var")
                self.text_segment.append(f"end_copy_var:")
        else:
            # Original logic for tally (integer) assignments
            temp_reg = self.get_temp_register()
            self.evaluate_expression(expression, temp_reg)
            self.text_segment.append(f"sw {temp_reg}, {variable}")

    def evaluate_expression(self, expression, target_reg):
        if expression['type'] == 'number':
            self.text_segment.append(f"li {target_reg}, {expression['value']}")
        elif expression['type'] == 'variable':
            self.text_segment.append(f"lw {target_reg}, {expression['name']}")
        elif expression['type'] == 'binary_operation':
            left_reg = self.get_temp_register()
            right_reg = self.get_temp_register()

            # Evaluate left and right operands
            self.evaluate_expression(expression['left'], left_reg)
            self.evaluate_expression(expression['right'], right_reg)

            # Perform the binary operation
            operator = expression['operator']
            if operator == 'augmented by':
                self.text_segment.append(f"add {target_reg}, {left_reg}, {right_reg}")
            elif operator == 'diminished by':
                self.text_segment.append(f"sub {target_reg}, {left_reg}, {right_reg}")
            elif operator == 'amplified by':
                self.text_segment.append(f"mul {target_reg}, {left_reg}, {right_reg}")
            elif operator == 'fragmented by':
                self.text_segment.append(f"div {left_reg}, {right_reg}")
                self.text_segment.append(f"mflo {target_reg}")

    def handle_input_statement(self ,node):
        variable = node['variable']
        var_info = self.symbol_table[variable]
        if var_info['data_type'] == "tally":
            self.text_segment.append(f"li $v0, 5")  # Read integer
            self.text_segment.append(f"syscall")
            self.text_segment.append(f"sw $v0, {variable}")
        elif var_info['data_type'] == "verse":
            buffer_label = self.get_buffer(variable)
            if f"{buffer_label}" not in self.data_segment:
                self.data_segment.append(f"{buffer_label}: .space 100") 
            
            self.text_segment.append(f"li $v0, 8")
            self.text_segment.append(f"la $a0, {buffer_label}")
            self.text_segment.append(f"li $a1, 100")
            self.text_segment.append(f"syscall")

    def handle_output_statement(self, node):
        for expr in node['expressions']:
            if expr['type'] == 'string':
                label = f"str_{len(self.data_segment)}"
                self.data_segment.append(f"{label}: .asciiz {expr['value']}")
                self.text_segment.append(f"la $a0, {label}")
                self.text_segment.append(f"li $v0, 4")  # Print string
            elif expr['type'] == 'variable':
                if self.symbol_table[expr['name']]['data_type'] == "verse":
                    buffer_label = self.get_buffer(expr['name'])
                    self.text_segment.append(f"la $a0, {buffer_label}")
                    self.text_segment.append(f"li $v0, 4")
                else:
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
    # input_code = """
    # int x;
    # cout << "Give me a number: ";
    # cin >> x;
    # int y;
    # y = x + 4;
    # cout << y;
    # """
    input_code = """
    verse x;
    verse y;
    cast spell "Enter value for x: ";
    summon x;
    cast spell "Enter value for y: ";
    summon y;
    cast spell x;
    cast spell y;
    """

    tokens = lexer.lexical_analyzer(input_code)
    parse_to_mips = parser.Parser(tokens)
    ast = parse_to_mips.parse()
    symbol_table = parse_to_mips.get_symbol_table()

    generator = Generator(symbol_table)
    mips_code = generator.generate_mips(ast)

    # output_file = "output.asm"
    # with open(output_file, "w") as file:
    #     file.write(mips_code)

    print(mips_code)

if __name__ == "__main__":
    main()
