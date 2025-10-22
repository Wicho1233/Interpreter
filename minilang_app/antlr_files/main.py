from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from test import EvalVisitor

def evaluate_code(code: str, visitor: EvalVisitor):
    input_stream = InputStream(code)
    lexer = MiniLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MiniLangParser(token_stream)
    tree = parser.program()
    visitor.visitProgram(tree)


def main():
    print("")

    visitor = EvalVisitor()
    buffer = "" 

    while True:
        try:
            line = input("->")

            if line.strip().lower() == "exit":
                print()
                break
            if line.strip() == "":
                if buffer.strip():
                    evaluate_code(buffer, visitor)
                    buffer = " "
            else:
                buffer += line + "\n"

        except KeyboardInterrupt:
            break



main()
