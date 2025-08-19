from lexer import Lexer
from parser import Parser

def validate_c_program(input_text):
    try:
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        is_valid = parser.parse()
        if is_valid:
            print("Valid C program!")
        return is_valid
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Example usage
if __name__ == "__main__":
    # Test original valid program
    print("Testing original valid program:")
    original_valid_program = read_file('valid_program.c')
    is_valid = validate_c_program(original_valid_program)
    print(f"Program is {'valid' if is_valid else 'invalid'}\n")
    
    # Test simple float program
    print("Testing simple float program:")
    simple_float_program = read_file('test_float_program.c')
    is_valid = validate_c_program(simple_float_program)
    print(f"Program is {'valid' if is_valid else 'invalid'}\n")
    
    # Test complex float program
    print("Testing complex float program:")
    complex_float_program = read_file('complex_float_program.c')
    is_valid = validate_c_program(complex_float_program)
    print(f"Program is {'valid' if is_valid else 'invalid'}\n")
    
    # Test invalid program
    print("Testing invalid program:")
    invalid_program = read_file('invalid_program.c')
    is_valid = validate_c_program(invalid_program)
    print(f"Program is {'valid' if is_valid else 'invalid'}\n") 