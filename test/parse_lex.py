import re
import ply.lex as lex
import ply.yacc as yacc

## Lexer part
tokens = ( 'LETTER', 'DIGIT', 'SEMI' )

t_LETTER = r'[a-z]'

def t_DIGIT(t):
    r'[0-9]'
    t.value = int(t.value)
    return t

t_SEMI = r';'
t_ignore = r' '

lexer = lex.lex(debug=1)

## Parser part
start = 'start'

def p_letter_digit_pair(p):
    ''' pair : LETTER DIGIT SEMI '''
    p[0] = (p[1], p[2])

def p_pair_group(p):
    ''' pair_group : pair_group pair
                   | pair
    '''
    print(p[0], p[1])
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

start = 'pair_group'

parser = yacc.yacc(debug=1)

## Test it
s = "a 0; b 1; c 2;"
print(parser.parse(s))
