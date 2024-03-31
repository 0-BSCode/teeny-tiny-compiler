from lex import *
from token_helper import *

def main():
    # source = "LET foobar = 123"
    # source = "+- */ >>= = != !"
    # source = "+- #This is a comment\n *"
    # source = "+- \"This is a string\" # This is a comment!\n */"
    # source = "+-123 9.8654*/"
    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.tokenKind != TokenType.EOF:
        print(token.tokenKind)
        token = lexer.getToken()

main()