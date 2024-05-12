#!/usr/bin/env python
import sys

# dependencies
from ply import lex, yacc

class Parser(object):
    def __init__(self):
        tokens = ("PAREN_OPEN", "PAREN_CLOSE", "BRACKET_OPEN", "BRACKET_CLOSE",
                  "BRACE_OPEN", "BRACE_CLOSE", "HORIZONTAL_WHITESPACE",
                  "VERTICAL_WHITESPACE", "IDENTIFIER")
        
        def t_PAREN_OPEN          (t): r"\("
        def t_PAREN_CLOSE         (t): r"\)"
        def t_BRACKET_OPEN        (t): r"\["
        def t_BRACKET_CLOSE       (t): r"\]"
        def t_BRACE_OPEN          (t): r"\{"
        def t_BRACE_CLOSE         (t): r"\}"
        def t_HORIZONAL_WHITESPACE(t): r"[ \t\r:,]+"; 
        def t_VERTICAL_WHITESPACE (t): r"\n+"; t.lexer.lineno += len(t.value)
    
        t_IDENTIFIER = (r"[^ \t\n\r\:\,\.\(\)\{\}\[\]0-9]"
                        r"[^ \t\n\r\:\,\.\(\)\{\}\[\]]*")
        
        def t_error(t):
            print("Illegal character '%s'" % t.value[0])
            t.lexer.skip(1)
        
        precedence = (
            ("left", "VERTICAL_WHITESPACE", "HORIZONTAL_WHITESPACE"),
        )
        
        def p_whitespace(p):
            """WHITESPACE : VERTICAL_WHITESPACE
                          | HORIZONTAL_WHITESPACE
                          | WHITESPACE WHITESPACE"""
            p[0] = p[1]
        
        def p_identifier(t): "expression : IDENTIFIER"; t[0] = Identifier(t[1])
        
        def p_list_inside(t):
            """list_inside : expression expression
                           | expression WHITESPACE expression
                           | list_inside expression
                           | expression list_inside"""
            if isinstance(list, t[1]):
                t[0] = List(t[1])
                t[0].append(t[2])
            elif isinstance(list, t[2]):
                t[0] = List([t[1]])
                t[0].extend(t[2])
            else:
                t[0] = List([t[1], t[2]])
        
        def p_list(t):
            """expression : PAREN_OPEN list_inside PAREN_CLOSE"""
            t[0] = List(t[2])
        
        def p_error(t):
            raise SyntaxError("Syntax error at '%s' (line %s)" % (t.value, t.lineno))
        
        self.lex = lex.lex()
        self.yacc = yacc.yacc()
    
    def __call__(self, s):
        self.lex.input(s)
        print list(self.lex)
        return self.yacc.parse(s)

class List(list):
    pass

class Identifier(str):
    pass

class String(str):
    __str__ = str.__repr__

print Parser()("foo")
