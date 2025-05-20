class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.current_char = self.input_text[0] if input_text else None
        self.tokens = []
        self.line = 1
        self.column = 1
        self.data_types = {'int', 'float'}

    def advance(self):
        self.position += 1
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
            self.column += 1
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            self.advance()

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            self.advance()  # Skip the newline

    def peek(self):
        peek_pos = self.position + 1
        if peek_pos >= len(self.input_text):
            return None
        return self.input_text[peek_pos]

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', int(result))

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if the identifier is a data type
        if result in self.data_types:
            return ('DATATYPE', result)
        # Check if the identifier is a keyword
        elif result in {'main', 'if', 'while', 'printf', 'scanf'}:
            return ('KEYWORD', result)
        # Otherwise it's a regular identifier (variable name)
        return ('IDENTIFIER', result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return ('EQUALS', '==')
                self.advance()
                return ('ASSIGN', '=')

            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return ('NOT_EQUALS', '!=')

            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return ('LESS_EQUALS', '<=')
                self.advance()
                return ('LESS', '<')

            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return ('GREATER_EQUALS', '>=')
                self.advance()
                return ('GREATER', '>')

            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')

            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')

            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')

            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')

            if self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')

            if self.current_char == '{':
                self.advance()
                return ('LBRACE', '{')

            if self.current_char == '}':
                self.advance()
                return ('RBRACE', '}')

            if self.current_char == ';':
                self.advance()
                return ('SEMICOLON', ';')

            if self.current_char == ',':
                self.advance()
                return ('COMMA', ',')

            if self.current_char == '&':
                self.advance()
                return ('AMPERSAND', '&')

            if self.current_char == '"':
                self.advance()
                return ('QUOTE', '"')

            if self.current_char == '%':
                self.advance()
                return ('PERCENT', '%')

            raise Exception(f'Invalid character: {self.current_char} at line {self.line}, column {self.column}')

        return ('EOF', None)

    def tokenize(self):
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            if token[0] == 'EOF':
                break
        return self.tokens 