from collections import namedtuple
from enum import Enum

class TokenKind(Enum):
    EOF = -1
    DEFINE = -2
    EXTERN = -3
    IDENTIFIER = -4
    NUMBER = -5
    OPERATOR = -6

Token = namedtuple('Token', 'kind value')

class Lexer(object):
    def __init__(self, buf):
        assert len(buf) >= 1
        self.buffer = buf
        self.pos = 0
        self.lastchar = self.buffer[0]

    def advance(self):
        """
        Advance steps forward in the incoming buffer. If this fails, return the empty string.
        """
        try:
            self.pos += 1
            self.lastchar = self.buffer[self.pos]
        except IndexError:
            self.lastchar = ''

    def tokens(self):
        """
        Tokens is a generator which produces tokens from the incoming buffer. Walk through each of the case classes carefully.
        """
        while self.lastchar:
            while self.lastchar.isspace():
                self.advance()

            if self.lastchar.isalpha():
                id_str = ''
                while self.lastchar.isalnum():
                    id_str += self.lastchar
                    self.advance()

                if id_str == 'define':
                    yield Token(kind = TokenKind.DEFINE, value = id_str)

                elif id_str == 'extern':
                    yield Token(kind = TokenKind.EXTERN, value = id_str)

                else:
                    yield Token(kind = TokenKind.IDENTIFIER, value = id_str)

            elif self.lastchar.isdigit() or self.lastchar == '.':
                num_str = ''
                while self.lastchar.isdigit() or self.lastchar == '.':
                    num_str += self.lastchar
                    self.advance()

                yield Token(kind = TokenKind.NUMBER, value = num_str)

            elif self.lastchar == '#':
                self.advance()
                while self.lastchar and self.lastchar not in '\r\n':
                    self.advance()

            elif self.lastchar:
                yield Token(kind = TokenKind.OPERATOR, value = self.lastchar)
                self.advance()

        yield Token(kind = TokenKind.EOF, value = '')
