from lexer import Lexer

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.tokens = lexer.tokenize()
        self.current_token_index = 0
        self.current_token = self.tokens[0]

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = ('EOF', None)

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise Exception(f'Expected {token_type}, got {self.current_token[0]} at token index {self.current_token_index}: {self.current_token}')

    def program(self):
        self.eat('DATATYPE')  # int
        self.eat('KEYWORD')   # main
        self.eat('LPAREN')    # (
        self.eat('RPAREN')    # )
        self.eat('LBRACE')    # {
        self.declarations()   # <Declaraciones>
        self.statements()     # <Enunciados>
        self.eat('RBRACE')    # }

    def declarations(self):
        while self.current_token[0] == 'DATATYPE':
            self.declaration()
            if self.current_token[0] != 'DATATYPE':
                break

    def declaration(self):
        self.eat('DATATYPE')  # tipo-dato
        self.variable_list()
        self.eat('SEMICOLON')

    def variable_list(self):
        self.eat('IDENTIFIER')  # nombre-variable
        while self.current_token[0] == 'COMMA':
            self.eat('COMMA')
            self.eat('IDENTIFIER')

    def statements(self):
        while self.current_token[0] in ['IDENTIFIER', 'KEYWORD']:
            if self.current_token[0] == 'KEYWORD' and self.current_token[1] not in ['if', 'while', 'printf', 'scanf']:
                break
            self.statement()
            if self.current_token[0] not in ['IDENTIFIER', 'KEYWORD']:
                break

    def statement(self):
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek()[0] == 'ASSIGN':
                self.assignment()
            else:
                raise Exception(f'Invalid statement at token index {self.current_token_index}: {self.current_token}')
        elif self.current_token[0] == 'KEYWORD':
            if self.current_token[1] == 'scanf':
                self.read()
            elif self.current_token[1] == 'printf':
                self.write()
            elif self.current_token[1] == 'if':
                self.if_statement()
            elif self.current_token[1] == 'while':
                self.while_statement()
            else:
                raise Exception(f'Invalid keyword at token index {self.current_token_index}: {self.current_token}')
        else:
            raise Exception(f'Invalid statement start at token index {self.current_token_index}: {self.current_token}')

    def peek(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return ('EOF', None)

    def assignment(self):
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        self.expression()
        self.eat('SEMICOLON')

    def read(self):
        self.eat('KEYWORD')  # scanf
        self.eat('LPAREN')
        self.eat('QUOTE')
        self.eat('PERCENT')
        self.eat('IDENTIFIER')  # d or f
        self.eat('QUOTE')
        self.eat('COMMA')
        self.eat('AMPERSAND')
        self.eat('IDENTIFIER')
        self.eat('RPAREN')
        self.eat('SEMICOLON')

    def write(self):
        self.eat('KEYWORD')  # printf
        self.eat('LPAREN')
        self.eat('QUOTE')
        self.eat('PERCENT')
        self.eat('IDENTIFIER')  # d or f
        self.eat('QUOTE')
        self.eat('COMMA')
        self.eat('IDENTIFIER')
        self.eat('RPAREN')
        self.eat('SEMICOLON')

    def if_statement(self):
        self.eat('KEYWORD')  # if
        self.eat('LPAREN')
        self.condition()
        self.eat('RPAREN')
        self.eat('LBRACE')
        self.statements()
        self.eat('RBRACE')

    def while_statement(self):
        self.eat('KEYWORD')  # while
        self.eat('LPAREN')
        self.condition()
        self.eat('RPAREN')
        self.eat('LBRACE')
        self.statements()
        self.eat('RBRACE')

    def condition(self):
        if self.current_token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        else:
            self.eat('NUMBER')
        
        if self.current_token[0] in ['EQUALS', 'NOT_EQUALS', 'LESS', 'GREATER', 'LESS_EQUALS', 'GREATER_EQUALS']:
            self.eat(self.current_token[0])
        else:
            raise Exception(f'Expected comparison operator, got {self.current_token[0]} at token index {self.current_token_index}: {self.current_token}')

        if self.current_token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        else:
            self.eat('NUMBER')

    def expression(self):
        if self.current_token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        else:
            self.eat('NUMBER')

        if self.current_token[0] in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
            self.eat(self.current_token[0])
            if self.current_token[0] == 'IDENTIFIER':
                self.eat('IDENTIFIER')
            else:
                self.eat('NUMBER')

    def format_token_layout(self):
        indent = 0
        layout = []
        current_line = []
        
        for token in self.tokens:
            if token[0] == 'EOF':
                break
                
            if token[0] == 'LBRACE':
                if current_line:
                    layout.append('    ' * indent + ' '.join(current_line))
                    current_line = []
                layout.append('    ' * indent + '{')
                indent += 1
            elif token[0] == 'RBRACE':
                if current_line:
                    layout.append('    ' * indent + ' '.join(current_line))
                    current_line = []
                indent -= 1
                layout.append('    ' * indent + '}')
            elif token[0] == 'SEMICOLON':
                current_line.append(';')
                layout.append('    ' * indent + ' '.join(current_line))
                current_line = []
            else:
                current_line.append(str(token[1]))
        
        return '\n'.join(layout)

    def parse(self):
        try:
            self.program()
            if self.current_token[0] != 'EOF':
                raise Exception(f'Unexpected tokens after program end at token index {self.current_token_index}: {self.current_token}')
            print("\nToken layout:")
            print(self.format_token_layout())
            print("\nParse completed successfully!")
            return True
        except Exception as e:
            print(f"\nParse error: {e}")
            print("\nToken layout up to error:")
            print(self.format_token_layout())
            return False 