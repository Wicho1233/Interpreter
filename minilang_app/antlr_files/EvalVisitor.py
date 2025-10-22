from antlr4 import *
from .MiniLangParser import MiniLangParser
from .MiniLangVisitor import MiniLangVisitor

class EvalVisitor(MiniLangVisitor):
    def __init__(self):
        self.variables = {}
        self.output = []
    
    def get_output(self):
        return self.output
    
    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)
        return self.variables
    
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)
    
    def visitAssign(self, ctx):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.variables[var_name] = value
        return value
    
    def visitPrint(self, ctx):
        value = self.visit(ctx.expr())
        self.output.append(str(value))
        return value
    
    def visitExpr(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        
        if ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise NameError(f"Variable '{var_name}' not defined")
        
        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() == '(':
                return self.visit(ctx.expr(0))
            
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            op = ctx.op.text
            
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
        
        return 0