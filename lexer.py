class LexicalError(Exception): pass
class SyntaxError(Exception): pass

class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"

class Token:
    __slots__ = ("type", "value")
    def __init__(self, type_, value): self.type, self.value = type_, value
    def __repr__(self): return f"Token({self.type}, {self.value!r})"

class Lexer:
    TOKEN_MAP = {'+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MUL, 
                '/': TokenType.DIV, '(': TokenType.LPAREN, ')': TokenType.RPAREN}
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace(): 
            self.advance()

    def integer(self):
        buffer = []
        while self.current_char and self.current_char.isdigit():
            buffer.append(self.current_char)
            self.advance()
        return int(''.join(buffer))

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            if token_type := self.TOKEN_MAP.get(self.current_char):
                char = self.current_char
                self.advance()
                return Token(token_type, char)
            raise LexicalError(f"Невідомий символ: {self.current_char!r}")
        return Token(TokenType.EOF, None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Очікувався {token_type}, отримано {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result
        self.eat(TokenType.INTEGER)
        return token.value

    def term(self):
        result = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                result *= self.factor()
            else:
                self.eat(TokenType.DIV)
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            else:
                self.eat(TokenType.MINUS)
                result -= self.term()
        return result

def main():
    while True:
        try:
            text = input('Введіть вираз (або "exit"): ').strip()
            if text.lower() == "exit": break
            if not text: continue
            
            lexer = Lexer(text)
            parser = Parser(lexer)
            result = parser.expr()
            print(f"Результат: {result}")
            
        except Exception as e:
            print(f"Помилка: {e}")

if __name__ == "__main__":
    main()