#!/usr/bin/env python
# encoding=utf-8

"""
Topic:下降解析器
"""
import re
import collections

# Token spec

NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>\-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

PATTERNS = re.compile(
    '|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS])
)

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])


def gen_tokens(text):
    "generate tokens"
    scanner = PATTERNS.scanner(text)

    for matched in iter(scanner.match, None):
        tok = Token(matched.lastgroup, matched.group())
        if tok.type != 'WS':
            yield tok

# Parser


class Evaluator(object):
    '''
    Implemention of a recursive decent parser
    '''

    def __init__(self):
        self.tokens = None
        self.tok = None
        self.nexttok = None

    def parse(self, text):
        '''
        parse code
        '''
        self.tokens = gen_tokens(text)
        self._advance()
        return self.expr()

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Test and consume the next token if it match toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        return False

    def _expect(self, toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('ExPected' + toktype)
    # Grammar rules follow

    def expr(self):
        '''
        expression::= term { ( '+'|'-' ) term}*
        '''
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            oprator = self.tok.type
            right = self.term()
            if oprator == 'PLUS':
                exprval += right
            elif oprator == 'NIMUS':
                exprval -= right

        return exprval

    def term(self):
        "term :: = factor { (('*')|('/')) factor }* "
        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            oprator = self.tok.type
            right = self.factor()
            if oprator == 'TIMES':
                termval *= right
            elif oprator == 'DIVIDE':
                termval /= right
        return termval

    def factor(self):
        "factor :: = NUM | (expr) "
        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')



