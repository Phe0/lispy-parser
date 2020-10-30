import re
from lark import Lark, InlineTransformer
from typing import NamedTuple


class Symbol(NamedTuple):
    value: str


grammar = Lark(r"""
    start : expr

    ?expr  : atom
           | func
           | list
           | quoted

    quoted : "'" expr

    func   : "(" SYMBOL expr+ ")"
           | "(" NAME expr+ ")"

    list   : "(" expr+ ")"


    ?atom  : STRING
           | SYMBOL
           | NUMBER
           | BOOLEAN
           | NAME
           | CHAR

    STRING : /"([^"\\\n\r\b\f]+|\\["\\\/bfnrt]|\\u[0-9a-fA-F]{4})*"/
    SYMBOL: /[-+=\/*!@$^&~<>?]+/
    NUMBER : /-?\d+(\.\d+)?/
    BOOLEAN: /\#t|\#nil/
    NAME   : /[a-zA-Z][-?\w]*/
    CHAR   : /\#[\w\\]+/
    %ignore /\s+/
    %ignore /;[^\n]*/
""")


class LispyTransformer(InlineTransformer):
    CHARS = {
        "altmode": "\x1b",
        "backnext": "\x1f",
        "backspace": "\b",
        "call": "SUB",
        "linefeed": "\n",
        "page": "\f",
        "return": "\r",
        "rubout": "\xc7",
        "space": " ",
        "tab": "\t",
    }
    def string(self, token):
        return eval(token)

    # def number(self, token):
    #     return float(token)
    
    # def boolean(self, token):
    #     return True if token.value == "#t" else False


exprs = [
    "((x 1))",
    "((x 1) (y 2))",
    "(let ((x 1) (y 2)) (+ x y))",
    "((1 2 3) (3 2 1))",
    "((diff cos) x)",
    "(let 1 2)"
]

for src in exprs:
    tree = grammar.parse(src)
    print(src)
    print(tree.pretty())
    print('-' * 40)