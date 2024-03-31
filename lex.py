from token_helper import *
import sys
class Lexer:
    def __init__(self, source):
        self.source = source + '\n' # Source code to lex as a string. Append newline to simplify lexing last statement.
        self.curChar = '' # Current character in the string.
        self.curPos = -1 # Current position in the string.
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        lookAheadPos = self.curPos + 1
        if lookAheadPos >= len(self.source):
            return '\0'
        return self.source[lookAheadPos]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("[LEXING ERROR] " + message)

    # Skip whitespace except newlines since newlines
    # indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()

    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        # Check first character of this token to see if we can figure out what it is.
        # If it is a multiple character operator (e.g., !=), number, keyword, or identifer,
        # then we will process the rest

        # Single-character operators
        if self.curChar == "+": # Addition token
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-": # Subtraction token.
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*": # Multiplication token
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/": # Division token
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "\n": # Newline token
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0": # EOF token
            token = Token('', TokenType.EOF)
        
        # Multi-character operators
        elif self.curChar == "=":
            # Check if it's = (assignment) or == (equality)
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == ">":
            # Check if it's >= (gteq) or > (gt)
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == "<":
            # Check if it's <= (lteq) or < (lt)
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        
        # Strings
        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string.
                # No escape characters, newlines, tabs, or % since
                # we'll use C's printf function to display the string.
                if self.curChar in ["\r", "\t", "\n", "\\", "%"]:
                    self.abort("Illegal character in string: " + self.curChar)
                self.nextChar()
            
            tokenText = self.source[startPos : self.curPos] # Get substring.
            token = Token(tokenText, TokenType.STRING)
        
        # Numbers
        elif self.curChar.isdigit():
            # Leading character is a digit, so token must be a number.
            # Get all consecutive digits (and decimal if there is one).
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            
            # Check for decimal.
            if self.peek() == ".":
                self.nextChar()

                if not self.peek().isdigit():
                    # Not a valid number.
                    self.abort("Illegal character in number: " + self.curChar)
                
                while self.peek().isdigit():
                    self.nextChar()
            
            tokenText = self.source[startPos: self.curPos + 1]
            token = Token(tokenText, TokenType.NUMBER)

        # Identifiers or keywords
        elif self.curChar.isalpha():
            # Leading character is a letter.
            startPos = self.curPos
            
            # Get all consecutive alphanumeric characters.
            while self.peek().isalnum():
                self.nextChar()
            
            tokenText = self.source[startPos: self.curPos + 1]
            keyword = Token.isKeyword(tokenText)
            if keyword == None:
                token = Token(tokenText, TokenType.IDENT)
            else:
                token = Token(tokenText, keyword)
        else: # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token